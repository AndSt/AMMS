from src.version_manager import VersionManager


# TODO: Add more examples: How to handle .x comparisons?

def test_init():
    examples = ['1_0', '1_x', '1_0_1']
    for example in examples:
        version = VersionManager(example)


def test_is_equal():
    examples = [
        ('1.0', '1_0'),
        ('1', '1_0_0'),
        ('1.1.0', '1.1'),
        ('1.x', '1.x.5'),
        ('1.x', '1.x.x')
    ]
    for example in examples:
        version = VersionManager(example[0])
        other = VersionManager(example[1])
        assert version == other
        assert version.__eq__(example[1])


def test_is_compatible_and_newer():
    # test whether 2nd entry is compatible and newer than first entry
    examples = [
        ('1.0', '1_0', False),
        ('1', '2.0', False),
        ('1.3', '1.5.2', True),
        ('1.3', '1.3.2', True),
        ('1.3.4', '1.3.8', True)
    ]
    for example in examples:
        version = VersionManager(example[0])
        other = VersionManager(example[1])
        print(version.tostr(), other.tostr(), example[2])
        assert version.is_compatible_and_newer(other) == example[2]

    x_test = ('1.x', '1.5.7')
    try:
        VersionManager(x_test[1]).is_compatible_and_newer(x_test[0])
        assert False
    except ValueError:
        assert True


def test_from_file_name():
    examples = [
        ('simple_text-1_0_1-1588436916.135168.pbz2', '1.0.1'),
        ('simplt-1_x-1588110709.491364.pbz2', '1.x')
    ]
    for example in examples:
        version = VersionManager.from_file_name(example[0])
        assert version.__eq__(VersionManager(example[1]))
        assert version.__eq__(example[1])

# TODO test stringifiers
