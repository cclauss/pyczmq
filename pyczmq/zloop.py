from pyczmq._cffi import ffi, C, ptop, nullable

ffi.cdef('''
/*  =========================================================================
    zloop - event-driven reactor

    -------------------------------------------------------------------------
    Copyright (c) 1991-2013 iMatix Corporation <www.imatix.com>
    Copyright other contributors as noted in the AUTHORS file.

    This file is part of CZMQ, the high-level C binding for 0MQ:
    http://czmq.zeromq.org.

    This is free software; you can redistribute it and/or modify it under
    the terms of the GNU Lesser General Public License as published by the 
    Free Software Foundation; either version 3 of the License, or (at your 
    option) any later version.

    This software is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABIL-
    ITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General 
    Public License for more details.

    You should have received a copy of the GNU Lesser General Public License 
    along with this program. If not, see <http://www.gnu.org/licenses/>.
    =========================================================================
*/

typedef struct
{
    void *socket;
    int fd;
    short events;
    short revents;
} zmq_pollitem_t;

//  Opaque class structure
typedef struct _zloop_t zloop_t;

//  @interface
//  Callback function for reactor events
typedef int (zloop_fn) (zloop_t *loop, zmq_pollitem_t *item, void *arg);

//  Create a new zloop reactor
 zloop_t *
    zloop_new (void);

//  Destroy a reactor
 void
    zloop_destroy (zloop_t **self_p);

//  Register pollitem with the reactor. When the pollitem is ready, will call
//  the handler, passing the arg. Returns 0 if OK, -1 if there was an error.
//  If you register the pollitem more than once, each instance will invoke its
//  corresponding handler.
 int
    zloop_poller (zloop_t *self, zmq_pollitem_t *item, zloop_fn handler, void *arg);

//  Cancel a pollitem from the reactor, specified by socket or FD. If both
//  are specified, uses only socket. If multiple poll items exist for same
//  socket/FD, cancels ALL of them.
 void
    zloop_poller_end (zloop_t *self, zmq_pollitem_t *item);

//  Configure a registered pollitem to ignore errors. If you do not set this, 
//  then pollitems that have errors are removed from the reactor silently.
 void
    zloop_set_tolerant (zloop_t *self, zmq_pollitem_t *item);

//  Register a timer that expires after some delay and repeats some number of
//  times. At each expiry, will call the handler, passing the arg. To
//  run a timer forever, use 0 times. Returns 0 if OK, -1 if there was an
//  error.
 int
    zloop_timer (zloop_t *self, size_t delay, size_t times, zloop_fn handler, void *arg);

//  Cancel all timers for a specific argument (as provided in zloop_timer)
 int
    zloop_timer_end (zloop_t *self, void *arg);

//  Set verbose tracing of reactor on/off
 void
    zloop_set_verbose (zloop_t *self, bool verbose);

//  Start the reactor. Takes control of the thread and returns when the 0MQ
//  context is terminated or the process is interrupted, or any event handler
//  returns -1. Event handlers may register new sockets and timers, and
//  cancel sockets. Returns 0 if interrupted, -1 if cancelled by a handler.
 int
    zloop_start (zloop_t *self);

//  Self test of this class
 void
    zloop_test (bool verbose);
''')

POLLIN = 1
POLLOUT = 2
POLLERR = 4

def new():
    loop = C.zloop_new()
    def destroy(c):
        C.zloop_destroy(ptop('zloop_t', c))
    return ffi.gc(loop, destroy)

def item(**kwargs):
    return ffi.new('zmq_pollitem_t', kwargs)

poller = C.zloop_poller
poller_end = C.zloop_poller_end
set_tolerant = C.zloop_set_tolerant
timer = C.zloop_timer
timer_end = C.zloop_timer_end
set_verbose = C.zloop_set_verbose
start = C.zloop_start
test = C.zloop_test
