
/* (c)  oblong industries */

// Installed under {{g_speak_home}}
#include "libGreenhouse2/Greenhouse.h"

using namespace oblong::staging2;


/**

  Please begin by consulting README.md

  To configure, build, and run the program, we recommend using obi.

      $ obi go

  To configure command line arguments, environment variables, and other launch
  settings, edit the project.yaml file.

 */

void Setup ()
{ auto t = new GHText ("Hello Greenhouse2!");
  SlapOnFeld (t);
}
