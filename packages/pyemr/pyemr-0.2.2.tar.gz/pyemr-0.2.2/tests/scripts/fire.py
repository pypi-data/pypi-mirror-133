import fire


def main(strarg: str, intarg: int, floatarg: float, boolarg: bool, *args, **kwargs):
    """

    Args:
      strarg:str:
      intarg:int:
      floatarg:float:
      boolarg:bool:
      *args:
      **kwargs:

    Returns:

    """
    assert type(intarg) == int
    assert type(floatarg) == float
    assert type(strarg) == str
    assert type(boolarg) == bool
    assert type(args) == list
    assert type(kwargs) == dict

    print(f"intarg={intarg}")
    print(f"floatarg={floatarg}")
    print(f"strarg={strarg}")
    print(f"boolarg={boolarg}")
    print(f"args={args}")
    print(f"kwargs={kwargs}")


if __name__ == "__main__":
    fire.Fire(main)
