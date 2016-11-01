#
# Copyright (c) 2014, 2016, Oracle and/or its affiliates. All rights reserved.
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
#
# This code is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 only, as
# published by the Free Software Foundation.
#
# This code is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# version 2 for more details (a copy is included in the LICENSE file that
# accompanied this code).
#
# You should have received a copy of the GNU General Public License version
# 2 along with this work; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Please contact Oracle, 500 Oracle Parkway, Redwood Shores, CA 94065 USA
# or visit www.oracle.com if you need additional information or have any
# questions.
#
suite = {
  "mxversion" : "5.34.4",
  "name" : "fastr",
  "versionConflictResolution" : "latest",
  "imports" : {
    "suites" : [
            {
               "name" : "truffle",
               "version" : "3c34543a8b7ff5edd74b76aafbeb3af52bd4afe7",
               "urls" : [
                    {"url" : "https://github.com/graalvm/truffle", "kind" : "git"},
                    {"url" : "https://curio.ssw.jku.at/nexus/content/repositories/snapshots", "kind" : "binary"},
                ]
            },

        ],
   },

  "repositories" : {
    "snapshots" : {
        "url" : "https://FASTR_SNAPSHOT_HOST/nexus/content/repositories/snapshots",
        "licenses" : ["GPLv2"]
    }
  },

  "licenses" : {
    "GPLv2" : {
      "name" : "GNU General Public License, version 2",
      "url" : "http://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html"
    },
  },

  "defaultLicense" : "GPLv2",

  # libraries that we depend on
  # N.B. The first four with a "path" attribute must be located
  # relative to the suite root and not the mx cache because they are
  # explicitly referenced in the Parser annotation processor.
  "libraries" : {
    "GNUR" : {
        "path" : "libdownloads/R-3.3.0.tar.gz",
        "urls" : ["http://cran.rstudio.com/src/base/R-3/R-3.3.0.tar.gz"],
        "sha1" : "166a25a7996150c9c83cdafcc89bfcd81578a887",
        "resource" : "true"
    },

    "GNU_ICONV" : {
        "path" : "libdownloads/libiconv-1.14.tar.gz",
        "urls" : ["http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.14.tar.gz"],
        "sha1" : "be7d67e50d72ff067b2c0291311bc283add36965",
        "resource" : "true"
    },

    "ANTLR-3.5" : {
      "path" : "libdownloads/antlr-runtime-3.5.jar",
      "urls" : ["http://central.maven.org/maven2/org/antlr/antlr-runtime/3.5/antlr-runtime-3.5.jar"],
      "sha1" : "0baa82bff19059401e90e1b90020beb9c96305d7",
    },

    "JDK_TOOLS" : {
      "path" : "${JAVA_HOME}/lib/tools.jar",
      "sha1" : "NOCHECK",
    },

    "ANTLR-C-3.5" : {
      "path" : "libdownloads/antlr-complete-3.5.1.jar",
      "urls" : ["http://central.maven.org/maven2/org/antlr/antlr-complete/3.5.1/antlr-complete-3.5.1.jar"],
      "sha1" : "ebb4b995fd67a9b291ea5b19379509160f56e154",
    },

  },

  "projects" : {
    "com.oracle.truffle.r.parser.processor" : {
      "sourceDirs" : ["src"],
      "dependencies" : [
        "JDK_TOOLS",
        "ANTLR-3.5",
        "ANTLR-C-3.5",
      ],
      "checkstyle" : "com.oracle.truffle.r.runtime",
      "javaCompliance" : "1.8",
      "workingSets" : "Truffle,FastR",
    },

    "com.oracle.truffle.r.parser" : {
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.r.parser.processor",
        "com.oracle.truffle.r.runtime",
      ],
      "checkstyle" : "com.oracle.truffle.r.runtime",
      "javaCompliance" : "1.8",
      "annotationProcessors" : ["TRUFFLE_R_PARSER_PROCESSOR"],
      "workingSets" : "Truffle,FastR",
    },

    "com.oracle.truffle.r.nodes" : {
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.r.runtime",
        "truffle:TRUFFLE_DEBUG",
      ],
      "checkstyle" : "com.oracle.truffle.r.runtime",
      "javaCompliance" : "1.8",
      "annotationProcessors" : [
          "truffle:TRUFFLE_DSL_PROCESSOR",
      ],
      "workingSets" : "Truffle,FastR",
      "jacoco" : "include",
    },

    "com.oracle.truffle.r.nodes.builtin" : {
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.r.library",
      ],
      "checkstyle" : "com.oracle.truffle.r.runtime",
      "javaCompliance" : "1.8",
      "annotationProcessors" : [
        "truffle:TRUFFLE_DSL_PROCESSOR",
      ],
      "workingSets" : "Truffle,FastR",
      "jacoco" : "include",
    },

    "com.oracle.truffle.r.nodes.test" : {
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.r.test",
      ],
      "checkstyle" : "com.oracle.truffle.r.runtime",
      "javaCompliance" : "1.8",
      "workingSets" : "Truffle,FastR,Test",
      "jacoco" : "include",
    },

    "com.oracle.truffle.r.test" : {
      "sourceDirs" : ["src"],
      "dependencies" : [
        "mx:JUNIT",
        "truffle:TRUFFLE_TCK",
        "com.oracle.truffle.r.engine",
      ],
      "checkstyle" : "com.oracle.truffle.r.runtime",
      "javaCompliance" : "1.8",
      "workingSets" : "Truffle,FastR,Test",
      "jacoco" : "include",
    },

    "com.oracle.truffle.r.test.native" : {
      "sourceDirs" : [],
      "dependencies" : ["com.oracle.truffle.r.native"],
      "class" : "FastRTestNativeProject",
      "native" : "true",
      "workingSets" : "FastR",
    },

    "com.oracle.truffle.r.test.cran" : {
      "sourceDirs" : ["r"],
      "javaCompliance" : "1.8",
      "workingSets" : "FastR",
    },

    "com.oracle.truffle.r.engine" : {
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.r.nodes.builtin",
        "com.oracle.truffle.r.parser",
        "truffle:JLINE",
        "truffle:TRUFFLE_DEBUG",
      ],
     "generatedDependencies" : [
        "com.oracle.truffle.r.parser",
     ],

      "annotationProcessors" : [
          "truffle:TRUFFLE_DSL_PROCESSOR",
      ],
      "checkstyle" : "com.oracle.truffle.r.runtime",
      "javaCompliance" : "1.8",
      "workingSets" : "Truffle,FastR",
      "jacoco" : "include",
    },

    "com.oracle.truffle.r.runtime" : {
      "sourceDirs" : ["src"],
      "dependencies" : [
        "truffle:TRUFFLE_API",
        "truffle:TRUFFLE_DEBUG",
      ],
      "checkstyle" : "com.oracle.truffle.r.runtime",
      "javaCompliance" : "1.8",
      "annotationProcessors" : [
          "truffle:TRUFFLE_DSL_PROCESSOR",
      ],
      "workingSets" : "Truffle,FastR",
      "jacoco" : "include",
    },

    "com.oracle.truffle.r.runtime.ffi" : {
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.r.runtime",
      ],
      "checkstyle" : "com.oracle.truffle.r.runtime",
      "javaCompliance" : "1.8",
      "workingSets" : "Truffle,FastR",
      "jacoco" : "include",
    },

    "com.oracle.truffle.r.native" : {
      "sourceDirs" : [],
      "dependencies" : [
        "GNUR",
        "GNU_ICONV",
      ],
      "native" : "true",
      "class" : "FastRNativeProject",
      "output" : "com.oracle.truffle.r.native",
      "workingSets" : "FastR",
    },

    "com.oracle.truffle.r.library" : {
      "sourceDirs" : ["src"],
      "dependencies" : [
        "com.oracle.truffle.r.nodes",
        "com.oracle.truffle.r.runtime.ffi",
      ],
      "annotationProcessors" : [
          "truffle:TRUFFLE_DSL_PROCESSOR",
      ],
      "checkstyle" : "com.oracle.truffle.r.runtime",
      "javaCompliance" : "1.8",
      "workingSets" : "FastR",
      "jacoco" : "include",

    },

    "com.oracle.truffle.r.release" : {
      "sourceDirs" : ["src"],
      "dependencies" : ["com.oracle.truffle.r.engine", "com.oracle.truffle.r.runtime.ffi", "com.oracle.truffle.r.native"],
      "class" : "FastRReleaseProject",
      "output" : "com.oracle.truffle.r.release"
    },
  },

  "distributions" : {
    "TRUFFLE_R_PARSER_PROCESSOR" : {
      "description" : "internal support for generating the R parser",
      "subDir" : "truffle",
      "dependencies" : ["com.oracle.truffle.r.parser.processor"],
      "exclude" : [
        "JDK_TOOLS",
        "ANTLR-3.5",
        "ANTLR-C-3.5",
       ],
       "maven" : "False",

    },

    "FASTR" : {
      "description" : "class files for compiling against FastR in a separate suite",
      "dependencies" : ["com.oracle.truffle.r.engine", "com.oracle.truffle.r.runtime.ffi"],
      "mainClass" : "com.oracle.truffle.r.engine.shell.RCommand",
      "exclude" : [
        "JDK_TOOLS",
        "truffle:JLINE",
        "ANTLR-C-3.5",
        "ANTLR-3.5",
        "GNUR",
        "GNU_ICONV",
      ],
      "distDependencies" : [
        "truffle:TRUFFLE_API",
        "truffle:TRUFFLE_DEBUG",
        "TRUFFLE_R_PARSER_PROCESSOR",
      ],
    },

    "FASTR_UNIT_TESTS" : {
      "description" : "unit tests",
      "dependencies" : ["com.oracle.truffle.r.test"],
      "exclude": ["mx:HAMCREST", "mx:JUNIT", "mx:JMH"],
      "distDependencies" : [
        "FASTR",
        "truffle:TRUFFLE_API",
        "truffle:TRUFFLE_DEBUG",
        "TRUFFLE_R_PARSER_PROCESSOR",
        "truffle:TRUFFLE_TCK",
      ],


    },

    "FASTR_UNIT_TESTS_NATIVE" : {
      "description" : "unit tests support (from test.native project)",
      "dependencies" : ["com.oracle.truffle.r.test.native"],
      "distDependencies" : ["FASTR_NATIVE_DEV"],
      "exclude" : ["GNUR", "GNU_ICONV"],
       "os_arch" : {
         "linux" : {
           "amd64" : {
             "path" : "mxbuild/dists/linux/amd64/fastr-unit-tests-native.jar",
           }
        },
         "darwin" : {
           "amd64" : {
             "path" : "mxbuild/dists/darwin/amd64/fastr-unit-tests-native.jar",
           },
        },
         "solaris" : {
           "amd64" : {
             "path" : "mxbuild/dists/solaris/amd64/fastr-unit-tests-native.jar",
           }
        },
      },
    },

    "FASTR_NATIVE_DEV": {
        "description" : "support for overriding the native project implementation in a separate suite",
        "dependencies" : ["com.oracle.truffle.r.native"],
        "exclude" : [
        "GNUR",
        "GNU_ICONV",
        ],
       "os_arch" : {
         "linux" : {
           "amd64" : {
             "path" : "mxbuild/dists/linux/amd64/fastr-native-dev.jar",
           },
        },
         "darwin" : {
           "amd64" : {
             "path" : "mxbuild/dists/darwin/amd64/fastr-native-dev.jar",
          },
        },
         "solaris" : {
           "amd64" : {
             "path" : "mxbuild/dists/solaris/amd64/fastr-native-dev.jar",
          },
        },
      },
    },

    "FASTR_RELEASE": {
      "description" : "a binary release of FastR",
      "dependencies" : ["com.oracle.truffle.r.release"],
       "os_arch" : {
         "linux" : {
           "amd64" : {
             "path" : "mxbuild/dists/linux/amd64/fastr-release.jar",
           }
        },
         "darwin" : {
           "amd64" : {
             "path" : "mxbuild/dists/darwin/amd64/fastr-release.jar",
           }
        },
         "solaris" : {
           "amd64" : {
             "path" : "mxbuild/dists/solaris/amd64/fastr-release.jar",
           }
        },
      },
    },
  },
}

