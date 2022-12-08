################################################################################
# COMPILE IBScanUltimate TEST APPLICATION
################################################################################

#
# ARCHITECTURE-DEPENDENT SETTINGS
#
ARCHFLAGS = -m64

#
# GENERAL SETTINGS
# CROSS_COMPILE MUST HAVE BEEN DEFINED AND EXPORTED
#
CC           = gcc
INCLUDES     = -I ../../../include
WARNINGS     = -Wall
OPTIMIZATION = -O2
LDFLAGS      = -L ../../../IBScanUltimate/lib
LIBRARIES    = -lstdc++ -lAKXUS -lpthread -lIBScanUltimate
DEFINES      = -DBSD -D__linux__ -D_MULTI_THREADED $(ARCHDEFINES)
FLAGSCC      = -fPIC $(ARCHFLAGS)
FLAGSAR      = -Wl,--no-as-needed $(ARCHFLAGS)

#
# DIRECTORIES AND NAMES OF OBJECTS TO BE CREATED
#
BINDIR = bin

OBJDIR = obj
OBJS_  = testScanU.o
OBJS   = $(patsubst %,$(OBJDIR)/%,$(OBJS_))

#
# TOP-LEVEL RULES
#
all: $(BINDIR)/testScanU

clean:
	rm -rf $(OBJDIR)
	rm -rf $(BINDIR)

#
# RULES FOR COMPILING DIRECTORIES OF OBJECTS
#
$(OBJS): | $(OBJDIR)
$(OBJDIR):
	mkdir $(OBJDIR)
$(OBJDIR)/%.o: %.cpp
	$(CC) $(OPTIMIZATION) $(INCLUDES) $(WARNINGS) $(DEFINES) $(FLAGSCC) -c -o $@ $<

#
# RULES FOR CREATING BINARIES
#
$(BINDIR)/testScanU: $(OBJS) | $(BINDIR)
	$(CC) $(OPTIMIZATION) $(FLAGSAR) -o $@ $^ $(LDFLAGS) $(LIBRARIES)
$(BINDIR):
	mkdir $(BINDIR)

