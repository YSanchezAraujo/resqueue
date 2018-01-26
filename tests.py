import utils

def main():
    assert test_reformat_input() == 0
    return None

def test_reformat_input():
    """test function for the function "reformat_input"
    in the file utils.py, if all is good return will be
    the integer zero {0}
    """
    msg = ("failed on case {}\ntest input was {}\n"
             "expected output was {}\nactual output is {}")
    tc1 = ["/this/is/a/silly/test", "/what/to/do"]
    tc2 = "/this/is/a/silly/test /what/to/do"
    test_dict = dict(case_one=dict(passed="not tested", test_case=tc1), 
                     case_two=dict(passed="not tested", test_case=tc2),
                     expected_output='"/this/is/a/silly/test /what/to/do"')
    test_dict["case_one"]["result"] = utils.reformat_input(tc1)
    test_dict["case_two"]["result"] = utils.reformat_input(tc2)
    if test_dict["expected_output"] != test_dict["case_one"]["result"]:
        test_dict["case_one"]["passed"] = False
        print(msg.format("one", tc1, test_dict["expected_output"],
                          test_dict["case_one"]["result"]))
        return test_dict["case_one"]
    if test_dict["expected_output"] != test_dict["case_two"]["result"]:
        test_dict["case_two"]["passed"] = False
        print(msg.format("two", tc2, test_dict["expected_output"], 
                         test_dict["case_two"]["result"]))
        return test_dict["case_two"]
    return 0

if __name__ == "__main__":        
    main()    
