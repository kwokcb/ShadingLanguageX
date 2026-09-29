//
// Options controlling how a MaterialX (MTLX) document is decompiled to SLX.
//

#ifndef MXSLC_DECOMPILEOPTIONS_H
#define MXSLC_DECOMPILEOPTIONS_H

#include "common.h"

namespace mxslc::decompile
{
    struct DecompileOptions
    {
        // Emit the `[[nodegraph]]` / `[[nodedef]]` function modifier above each
        // function produced from an MTLX nodegraph or nodedef. A graph that
        // implements a definition emits `[[nodedef]]`; a compound nodegraph emits
        // `[[nodegraph]]`. When false (default) no modifiers are emitted.
        bool emit_function_modifiers{false};
    };
}

#endif //MXSLC_DECOMPILEOPTIONS_H
