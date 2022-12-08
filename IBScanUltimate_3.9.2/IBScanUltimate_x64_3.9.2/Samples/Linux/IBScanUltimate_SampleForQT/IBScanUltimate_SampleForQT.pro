INCLUDEPATH += ./../../../include
INCLUDEPATH += ./../../../Lib
LIBS += -L"./../../../lib" -lIBScanUltimate

TEMPLATE = app
TARGET = IBScanUltimate_SampleForQT
DESTDIR = ./bin
QT += core gui

HEADERS += ./IBSU_SampleForQT.h ./TypeReDef.h
SOURCES += ./IBSU_SampleForQT.cpp ./main.cpp
FORMS += ./IBSU_SampleForQT.ui
RESOURCES += ./Images.qrc

CONFIG += static
CONFIG += release
CONFIG += warn_off
static {
CONFIG += static
DEFINES += STATIC
message("Static build.")
}