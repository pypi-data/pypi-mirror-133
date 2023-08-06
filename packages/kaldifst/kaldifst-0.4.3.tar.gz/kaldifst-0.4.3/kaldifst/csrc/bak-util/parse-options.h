// kaldifst/csrc/util/parse-options.h

// Copyright 2009-2011  Karel Vesely;  Microsoft Corporation;
//                      Saarland University (Author: Arnab Ghoshal);
// Copyright 2012-2013  Frantisek Skala;  Arnab Ghoshal

// See ../../COPYING for clarification regarding multiple authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//  http://www.apache.org/licenses/LICENSE-2.0
//
// THIS CODE IS PROVIDED *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
// WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
// MERCHANTABLITY OR NON-INFRINGEMENT.
// See the Apache 2 License for the specific language governing permissions and
// limitations under the License.

#ifndef KALDIFST_CSRC_UTIL_PARSE_OPTIONS_H_
#define KALDIFST_CSRC_UTIL_PARSE_OPTIONS_H_

#include <map>
#include <string>
#include <vector>


namespace kaldifst {

class ParseOptions {
 public:

  /// The following function will return a possibly quoted and escaped
  /// version of "str", according to the current shell.  Currently
  /// this is just hardwired to bash.  It's useful for debug output.
  static std::string Escape(const std::string &str);
};
}  // namespace kaldifst

#endif  // KALDIFST_CSRC_UTIL_PARSE_OPTIONS_H_
