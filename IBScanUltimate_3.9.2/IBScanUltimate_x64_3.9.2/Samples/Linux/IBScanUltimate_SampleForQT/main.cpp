#include <QtGui/QApplication>
#include "IBSU_SampleForQT.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    IBSU_SampleForQT dlg;
    dlg.show();
    
	int result = app.exec();
    return result;
}
