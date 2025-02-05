from lab_main.lab_app.models.storages import Storage
from lab_main.lab_app.models.users import User
from lab_main.lab_app.models.parameters import Parameter
from .objs_for_test import (
    user_for_tests,
    db_for_tests,
    storage_for_tests,
    zone_for_tests,
    param_for_test
)

session = db_for_tests()


def test_if_param_created():
    param = param_for_test()
    session.add(param)
    session.commit()
    param_from_db = session.query(Parameter).filter_by(id=param.id)
    assert param_from_db.id == param.id
    assert param_from_db.descrition == param.description    
