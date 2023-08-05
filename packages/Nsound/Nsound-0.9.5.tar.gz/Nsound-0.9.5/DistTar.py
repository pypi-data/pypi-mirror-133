# DistTarBuilder: tool to generate tar files using SCons
# Copyright (C) 2005, 2006  Matthew A. Nicholson
# Copyright (C) 2006  John Pye
#
# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 2.1 as published by the Free Software Foundation.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os,sys
from SCons.Script import *
import SCons.Builder

def DistTarEmitter(target,source,env):

    source,origsource = [], source

    excludeexts  = env.Dictionary().get('DISTTAR_EXCLUDE_EXTS',[])
    excludedirs  = env.Dictionary().get('DISTTAR_EXCLUDE_DIRS',[])
    excludefiles = env.Dictionary().get('DISTTAR_EXCLUDE_FILES',[])

    # assume the sources are directories... need to check that
    for item in origsource:

        if os.path.isdir(str(item)):

            dir_list = []
            dir_list.append(str(item))

            while len(dir_list) > 0:

                root = dir_list[0]

                for entry in os.listdir(root):

                    path = os.path.join(root,entry)

                    # Handle directory
                    if os.path.isdir(path):

                        add_path = True
                        for d in excludedirs:
                            if d in path:
                                add_path = False
                                break

                        if add_path:
                            dir_list.append(path)

                    # Handle file
                    else:

                        add_file = True
                        for ext in excludeexts:
                            if path.endswith(ext):
                                add_file = False
                                break

                        if add_file:
                            source.append(path)

                dir_list.pop(0)

    return target, source

def DistTarString(target, source, env):
   """
   This is what gets printed on the console. We'll strip out the list or source
   files, since it tends to get very long. If you want to see the contents, the
   easiest way is to uncomment the line 'Adding to TAR file' below.
   """
   return 'DistTar(%s,...)' % str(target[0])

def DistTar(target, source, env):
   """tar archive builder"""

   import tarfile

   env_dict = env.Dictionary()

   if env_dict.get("DISTTAR_FORMAT") in ["gz", "bz2"]:
      tar_format = env_dict["DISTTAR_FORMAT"]
   else:
      tar_format = ""

   # split the target directory, filename, and stuffix
   base_name = str(target[0]).split('.tar')[0]
   (target_dir, dir_name) = os.path.split(base_name)

   # create the target directory if it does not exist
   if target_dir and not os.path.exists(target_dir):
      os.makedirs(target_dir)

   # open our tar file for writing
   sys.stderr.write("DistTar: Writing "+str(target[0]))
   tar = tarfile.open(str(target[0]), "w:%s" % (tar_format,))

   # write sources to our tar file
   for item in source:
      item = str(item)
      sys.stderr.write(".")
      #print "Adding to TAR file: %s/%s" % (dir_name,item)
      tar.add(item,'%s/%s' % (dir_name,item))

   # all done
   sys.stderr.write("\n") #print "Closing TAR file"
   tar.close()

def DistTarSuffix(env, sources):
   """tar archive suffix generator"""

   env_dict = env.Dictionary()
   if env_dict.has_key("DISTTAR_FORMAT") and env_dict["DISTTAR_FORMAT"] in ["gz", "bz2"]:
      return ".tar." + env_dict["DISTTAR_FORMAT"]
   else:
      return ".tar"

def generate(env):
   """
   Add builders and construction variables for the DistTar builder.
   """

   env.Append(BUILDERS = {
      'DistTar': env.Builder(
         action = SCons.Action.Action(DistTar, DistTarString),
         suffix = DistTarSuffix,
         emitter = DistTarEmitter,
         target_factory = env.fs.Entry,
      ),
   })

   env.AppendUnique(
      DISTTAR_FORMAT = 'gz',
   )

def exists(env):
   """
   Make sure this tool exists.
   """
   try:
      import os
      import tarfile
   except ImportError:
      return False
   else:
      return True
