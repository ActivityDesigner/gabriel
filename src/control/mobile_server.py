#!/usr/bin/env python 
#
# Cloudlet Infrastructure for Mobile Computing
#
#   Author: Kiryong Ha <krha@cmu.edu>
#
#   Copyright (C) 2011-2013 Carnegie Mellon University
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import time
import sys

import SocketServer
import threading
import select
import traceback
import Queue
import struct
import socket

from config import Const as Const
import log as logging
from upnp_server import UPnPServer, UPnPError


LOG = logging.getLogger(__name__)
image_queue_list = list()
result_queue_list = list()


class MobileCommError(Exception):
    pass

class MobileVideoHandler(SocketServer.StreamRequestHandler, object):
    def setup(self):
        super(MobileVideoHandler, self).setup()
        self.average_FPS = 0.0
        self.current_FPS = 0.0
        self.init_connect_time = None
        self.previous_time = None
        self.current_time = 0
        self.frame_count = 0

    def _handle_image_input(self):
        img_size = self.request.recv(4)
        if img_size is None or len(img_size) != 4:
            msg = "Failed to receive first byte of header"
            raise MobileCommError(msg)
        img_size = struct.unpack("!I", img_size)[0]
        image_data = self.request.recv(img_size)
        while len(image_data) < img_size:
            image_data += self.request.recv(img_size - len(image_data))
        self.frame_count += 1

        # measurement
        self.current_time = time.time()
        self.current_FPS = 1 / (self.current_time - self.previous_time)
        self.average_FPS = self.frame_count / (self.current_time -
                self.init_connect_time)
        self.previous_time = self.current_time

        if (self.frame_count % 10 == 0):
            msg = "Video frame rate from client : current(%f), average(%f)" % \
                    (self.current_FPS, self.average_FPS)
            LOG.info(msg)
        for image_queue in image_queue_list:
            if image_queue.full() is True:
                image_queue.get()
            image_queue.put(image_data)

    def _handle_result_output(self):
        global result_queue_list

        for result_queue in result_queue_list:
            result_msg = None
            try:
                result_msg = result_queue.get_nowait()
            except Queue.Empty:
                pass
            if result_msg is not None:
                ret_size = struct.pack("!I", len(result_msg))
                self.request.send(ret_size)
                self.wfile.write(result_msg)
                self.wfile.flush()
                LOG.info("result message (%s) sent to the Glass", result_msg)

    def handle(self):
        global image_queue_list
        try:
            LOG.info("new Google Glass is connected")
            self.init_connect_time = time.time()
            self.previous_time = time.time()

            socket_fd = self.request.fileno()
            input_list = [socket_fd]
            output_list = [socket_fd]
            while True:
                inputready, outputready, exceptready = \
                        select.select(input_list, output_list, [])
                for s in inputready:
                    if s == socket_fd:
                        self._handle_image_input()
                for output in outputready:
                    if output == socket_fd:
                        self._handle_result_output()
                time.sleep(0.001)

        except Exception as e:
            LOG.info(traceback.format_exc())
            LOG.info("%s" % str(e))
            LOG.info("handler raises exception\n")
            LOG.info("Client disconnected")
            self.terminate()

    def terminate(self):
        pass


class MobileCommServer(SocketServer.TCPServer):
    def __init__(self, args):
        server_address = ('0.0.0.0', Const.MOBILE_SERVER_PORT)
        self.allow_reuse_address = True
        try:
            SocketServer.TCPServer.__init__(self, server_address,
                    MobileVideoHandler)
        except socket.error as e:
            sys.stderr.write(str(e))
            sys.stderr.write("Check IP/Port : %s\n" % (str(server_address)))
            sys.exit(1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        LOG.info("* Mobile server configuration")
        LOG.info(" - Open TCP Server at %s" % (str(server_address)))
        LOG.info(" - Disable nagle (No TCP delay)  : %s" %
                str(self.socket.getsockopt(
                    socket.IPPROTO_TCP,
                    socket.TCP_NODELAY)))
        LOG.info("-" * 50)

        # Start UPnP Server
        try:
            self.upnp_server = UPnPServer()
            self.upnp_server.start()
        except UPnPError as e:
            LOG.warning(str(e))
            LOG.warning("Cannot start UPnP Server")
            self.upnp_server = None
        LOG.info("Start UPnP Server")

    def handle_error(self, request, client_address):
        #SocketServer.TCPServer.handle_error(self, request, client_address)
        #sys.stderr.write("handling error from client")
        pass

    def terminate(self):
        # close all thread
        if self.socket != -1:
            self.socket.close()
        if hasattr(self, 'upnp_server') and self.upnp_server is not None:
            LOG.info("[TERMINATE] Terminate UPnP Server")
            self.upnp_server.terminate()
            self.upnp_server.join()
        if hasattr(self, 'rest_server') and self.rest_server is not None:
            LOG.info("[TERMINATE] Terminate REST API monitor")
            self.rest_server.terminate()
            self.rest_server.join()
        LOG.info("[TERMINATE] Finish mobile communication server connection")


def main():
    mobile_server = MobileCommServer(sys.argv[1:])

    LOG.info('started mobile server at %s' % (str(Const.MOBILE_SERVER_PORT)))
    mobile_server_thread = threading.Thread(target=mobile_server.serve_forever)
    mobile_server_thread.daemon = True

    try:
        mobile_server_thread.start()
    except Exception as e:
        sys.stderr.write(str(e))
        mobile_server.terminate()
        sys.exit(1)
    except KeyboardInterrupt as e:
        sys.stdout.write("Exit by user\n")
        mobile_server.terminate()
        sys.exit(1)
    else:
        mobile_server.terminate()
        sys.exit(0)


if __name__ == '__main__':
    main()