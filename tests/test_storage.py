import tempfile

from pgbackup import storage
import pytest
import tempfile

from pgbackup import storage

@pytest.fixture
def infile():
    f = tempfile.TemporaryFile('r+b')
    f.write(b"Testing")
    f.seek(0)
    return f


def test_local_storage(infile):

    outfile= tempfile.NamedTemporaryFile(delete=False)
    storage.local(infile,outfile)
    with open(outfile.name, 'rb') as f:
        assert f.read() == b'Testing'




def test_storing_file_on_s3(mocker, infile):
    client = mocker.Mock()
    storage.s3(client,infile,"bucket","file-name")

    client.upload_fileobj.assert_called_with(infile,"bucket","file-name")
