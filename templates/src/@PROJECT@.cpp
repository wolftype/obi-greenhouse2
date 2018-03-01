
/* (c)  oblong industries */

// Installed under {{g_speak_home}}
#include "libGreenhouse/Greenhouse.h"

using namespace oblong::staging;


/**

  Please begin by consulting README.md

  To configure, build, and run the program, we recommend using obi.

      $ obi go

  To configure command line arguments, environment variables, and other launch
  settings, edit the project.yaml file.

 */

void Setup ()
{ auto t = new Text ("Hello Greenhouse!");
  t -> SlapOnFeld ();
}