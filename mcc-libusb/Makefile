#############################################################################
#	                                                                    #
#	Makefile for building:                                              #
#                                                                           #
#		libmccusb.so:        Library for USB series                 #
#                                                                           #
#                                                                           #
#                                                                           #
#               Copyright (C)  2014-2016                                    #
#               Written by:  Warren J. Jasper                               #
#                            North Carolina State Univerisity               #
#                                                                           #
#############################################################################
#SRCS =    pmd.c  nist.c   usb-1608G.c usb-20X.c usb-1208FS-Plus.c usb-1608FS-Plus.c usb-2020.c  \
#          usb-ctr.c usb-2600.c usb-2408.c usb-2416.c usb-1608HS.c usb-1208HS.c usb-2001-tc.c    \
#          usb-1024LS.c usb-1208LS.c usb-1608FS.c usb-7202.c usb-tc.c usb-dio24.c usb-dio96H.c   \
#          usb-5200.c usb-temp.c usb-7204.c usb-1208FS.c usb-ssr.c usb-erb.c usb-pdiso8.c        \
#          usb-1408FS.c usb-1616FS.c usb-3100.c usb-4303.c usb-tc-ai.c usb-dio32HS.c usb-tc-32.c \
#          bth-1208LS.c minilab-1008.c
#HEADERS = pmd.h usb-500.h usb-1608G.h usb-20X.h usb-1208FS-Plus.h usb-1608FS-Plus.h usb-2020.h  \
#          usb-ctr.h usb-2600.h usb-2408.h usb-2416.h usb-1608HS.h usb-1208HS.h usb-2001-tc.h    \
#          usb-1024LS.h usb-1208LS.h usb-1608FS.h usb-7202.h usb-tc.h usb-dio24.h usb-dio96H.h   \
#          usb-5200.h usb-temp.h usb-7204.h usb-1208FS.h usb-ssr.h usb-erb.h usb-pdiso8.c        \
#          usb-1408FS.h usb-1616FS.h usb-3100.h usb-4303.h usb-tc-ai.h usb-dio32HS.h usb-tc-32.h \
#          bth-1208LS.h minilab-1008.h
#

#  Current Version of the driver
VERSION=1.17

SRCS =    pmd.c nist.c usb-2408.c
          
HEADERS = pmd.h usb-2408.h

OBJS = $(SRCS:.c=.o)   # same list as SRCS with extension changed
CC=gcc
CFLAGS+= -g -Wall -fPIC -O -I/usr/local/include/libusb-1.0 -L/usr/local/lib -lusb-1.0
ifeq ($(shell uname), Darwin)
	SONAME_FLAGS = -install_name
	SHARED_EXT = dylib
else
	SONAME_FLAGS = -soname
	SHARED_EXT = so
endif 
TARGETS=libmccusb.$(SHARED_EXT) libmccusb.a test-usb2408 jtest

ID=MCCLIBUSB
DIST_NAME=$(ID).$(VERSION).tgz
DIST_FILES={README,Makefile,nist.c,pmd.c,pmd.h,usb-2408.h,usb-2408.c,test-usb2408.c,jtest.c}

###### RULES
all: $(TARGETS)

%.d: %.c
	set -e; $(CC) -I. -M $(CPPFLAGS) $< \
	| sed 's/\($*\)\.o[ :]*/\1.o $@ : /g' > $@; \
	[ -s $@ ] || rm -f $@
ifneq ($(MAKECMDGOALS),clean)
include $(SRCS:.c=.d)
endif

libmccusb.$(SHARED_EXT): $(OBJS)
#	$(CC) -O -shared -Wall $(OBJS) -o $@
	$(CC) -shared -Wl,$(SONAME_FLAGS),$@ -o $@ $(OBJS) -lc -lm $(CFLAGS)

libmccusb.a: $(OBJS)
	ar -r libmccusb.a $(OBJS)
	ranlib libmccusb.a

#
# libusb-1.0
#

test-usb2408:	test-usb2408.c usb-2408.o libmccusb.a 
	$(CC) -g -Wall -I. -o $@ $@.c -L. -lmccusb  -lm -L/usr/local/lib -lhidapi-libusb -lusb-1.0 

jtest:		jtest.c usb-2408.o libmccusb.a 
	$(CC) -g -Wall -I. -o $@ $@.c -L. -lmccusb  -lm -L/usr/local/lib -lhidapi-libusb -lusb-1.0 

blinky:	blinky.c usb-2408.o libmccusb.a 
	$(CC) -g -Wall -I. -I/usr/include/python3.4 -o $@ $@.c -L. -lmccusb  -lm -L/usr/local/lib -lhidapi-libusb -lusb-1.0 


################ HID devices ##########################



####################################################################################################

clean:
	rm -rf *.d *.o *~ *.a *.so *.dylib *.dll *.lib *.dSYM $(TARGETS)

dist:	
	make clean
	cd ..; tar -zcvf $(DIST_NAME) mcc-libusb/$(DIST_FILES);

install:
	-install -d /usr/local/lib
	-install -c --mode=0755 ./libmccusb.a libmccusb.$(SHARED_EXT) /usr/local/lib
	-/bin/ln -s /usr/local/lib/libmccusb.$(SHARED_EXT) /usr/lib/libmccusb.$(SHARED_EXT)
	-/bin/ln -s /usr/local/lib/libmccusb.a /usr/lib/libmccusb.a
	-install -d /usr/local/include/libusb
	-install -c --mode=0644 ${HEADERS} /usr/local/include/libusb/

uninstall:
	-rm -f /usr/local/lib/libmccusb*
	-rm -f /usr/lib/libmccusb*
	-rm -rf /usr/local/include/libusb
