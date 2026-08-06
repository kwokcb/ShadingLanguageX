//
// Created by GitHub Copilot.
//

#include "statements/GeomInfoStatement.h"

#include "serialize/Serializer.h"
#include "statements/interface.h"

namespace mxslc::statements
{
    GeomInfoStatement::GeomInfoStatement(
        Token token,
        string name,
        string geom,
        vector<GeomPropDefinition> geom_props
    )
        : Statement{std::move(token)},
          name_{std::move(name)},
          geom_{std::move(geom)},
          geom_props_{std::move(geom_props)}
    {

    }

    StmtPtr GeomInfoStatement::monomorphize(const TypePtr& template_type) const
    {
        return create_statement<GeomInfoStatement>(token_, name_, geom_, geom_props_);
    }

    void GeomInfoStatement::execute_impl() const
    {
        const mx::GeomInfoPtr geom_info = serializer().document()->addGeomInfo(name_, geom_);
        for (const GeomPropDefinition& geom_prop : geom_props_)
        {
            const mx::GeomPropPtr prop = geom_info->addGeomProp(geom_prop.name);
            prop->setType(geom_prop.type);
            prop->setValueString(geom_prop.value);
        }
    }

    string GeomInfoStatement::to_string() const
    {
        string result = "geominfo(\"" + name_ + "\", \"" + geom_ + "\")";
        result += " {";
        for (const GeomPropDefinition& geom_prop : geom_props_)
            result += " geomprop(\"" + geom_prop.name + "\", \"" + geom_prop.type + "\", \"" + geom_prop.value + "\");";
        return result + " }";
    }
}