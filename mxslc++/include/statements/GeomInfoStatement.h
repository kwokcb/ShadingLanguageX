//
// Created by GitHub Copilot.
//

#ifndef MXSLC_GEOMINFOSTATEMENT_H
#define MXSLC_GEOMINFOSTATEMENT_H

#include "common.h"
#include "statements/Statement.h"

namespace mxslc::statements
{
    struct GeomPropDefinition
    {
        string name;
        string type;
        string value;
    };

    class GeomInfoStatement final : public Statement
    {
    public:
        GeomInfoStatement(Token token, string name, string geom, vector<GeomPropDefinition> geom_props);

        StmtPtr monomorphize(const TypePtr& template_type) const override;
        void execute_impl() const override;

        string to_string() const override;

    private:
        string name_;
        string geom_;
        vector<GeomPropDefinition> geom_props_;
    };
}

#endif //MXSLC_GEOMINFOSTATEMENT_H