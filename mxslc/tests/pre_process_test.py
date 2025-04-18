from mxslc.pre_process import pre_process


def test_pre_process_removes_comments():
    source = """
    int i = 0;
    // string s = "hello world"
    int j = 1; // TODO
    float f = 1.0;
    //if (true)
    //    do_something();
    """

    expected = """
    int i = 0;
    
    int j = 1; 
    float f = 1.0;
    
    
    """
    assert pre_process(source, []) == expected


def test_pre_process_removes_undefined_blocks():
    source = """
    int i = 0;
    int j = 0;
    #IF INCR_I
    i += 1;
    #ENDIF
    #IF INCR_J
    j += 1;
    #ENDIF
    #IF INCR_I
    i += 1;
    #ENDIF
    """

    expected = """
    int i = 0;
    int j = 0;
    j += 1;
    """
    assert pre_process(source, ["INCR_J"]) == expected

    expected = """
    int i = 0;
    int j = 0;
    i += 1;
    i += 1;
    """
    assert pre_process(source, ["INCR_I"]) == expected

    expected = """
    int i = 0;
    int j = 0;
    """
    assert pre_process(source, []) == expected
