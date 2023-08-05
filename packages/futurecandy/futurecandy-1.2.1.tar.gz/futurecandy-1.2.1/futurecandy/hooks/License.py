"""Python script for license.hook.futurecandy."""

import configparser
from sys import argv
from string import Template
from os.path import join, expanduser
from os import system
from ast import literal_eval
from datetime import date
import enquiries

config = configparser.ConfigParser()
config.read(join(expanduser("~"), ".futurecandy/candy.cfg"))

LICENSES = {
    "Closed": Template("Copyright (C) $year, $entity\nAll rights reserved."),
    "MIT": Template(
        "Copyright (C) $year $entity\n\nPermission is hereby granted, free of"
        " charge, to any person obtaining a copy of this software and "
        "associated documentation files " """(the "Software")""" ", to "
        "deal in the Software without restriction, including without "
        "limitation the rights to use, copy, modify, merge, publish, "
        "distribute, sublicense, and/or sell copies of the Software, "
        "and to permit persons to whom the Software is furnished to do "
        "so, subject to the following conditions: \n\nThe above "
        "copyright  notice and this permission notice shall be included"
        " in all copies or substantial portions of the Software.\n\n"
        "THE SOFTWARE IS PROVIDED """"AS IS"""", WITHOUT WARRANTY OF "
        "ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE"
        " WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR "
        "PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR "
        "COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER "
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR "
        "OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE "
        "SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."),
    "Apache 2.0": Template("""Copyright $year $entity

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.""")
}

if enquiries.confirm("Use template LICENSE?"):
    with open(join(argv[1], "LICENSE"), "w") as license_handle:
        license_handle.write(LICENSES[enquiries.choose(
            "Specify license: ", LICENSES.keys())].substitute({
                "year": str(date.today().year), "entity": enquiries.freetext(
                    "Specify copyright holder: ")}))
else:
    system(literal_eval(config["editors"]["light"]) + " " +
           join(argv[1], "LICENSE"))
