from ijim.text.tokenizer import TokenType, Tokenizer
from .key import *
import os

def _skip_to_next_key_section(tok: Tokenizer):
    t = tok.getToken()
    while t.type != TokenType.EOF and (t.type != TokenType.Identifier or t.value.upper() != "SECTION"):
        t = tok.getToken()

    if t.type != TokenType.EOF:
        tok.assertPunctuator(":")

def _parse_key_section_header(tok: Tokenizer, key: Key):
    tok.assertIdentifier("FLAGS")
    key.flags  = KeyFlag(tok.getIntNumber())

    tok.assertIdentifier("TYPE")
    key.type   = KeyType(tok.getIntNumber())

    tok.assertIdentifier("FRAMES")
    key.frames = tok.getIntNumber()

    tok.assertIdentifier("FPS")
    key.fps    = tok.getFloatNumber()

    tok.assertIdentifier("JOINTS")
    key.joints = tok.getIntNumber()

def _parse_key_section_markers(tok: Tokenizer, key: Key):
    tok.assertIdentifier("MARKERS")

    numMarkers = tok.getIntNumber()
    for i in range(0, numMarkers):
        m = KeyMarker()
        m.frame = tok.getFloatNumber()
        m.type  = KeyMarkerType(tok.getIntNumber())
        key.markers.append(m)

def _parse_key_section_keyframe_nodes(tok: Tokenizer, key: Key):
    tok.assertIdentifier("NODES")
    numNodes = tok.getIntNumber()
    for i in range(0, numNodes):
        node = KeyNode()

        tok.assertIdentifier("NODE")
        node.num = tok.getIntNumber()

        tok.assertIdentifier("MESH")
        tok.assertIdentifier("NAME")
        node.meshName = tok.getSpaceDelimitedString()

        tok.assertIdentifier("ENTRIES")
        numEntries = tok.getIntNumber()
        for j in range(0, numEntries):
            tok.assertInteger(j)
            tok.assertPunctuator(':')

            keyframe = Keyframe()
            keyframe.frame = tok.getIntNumber()
            keyframe.flags = KeyframeFlag(tok.getIntNumber())

            keyframe.position = tok.getVector3f()
            keyframe.orientation = tok.getVector3f()
            keyframe.deltaPosition = tok.getVector3f()
            keyframe.deltaRotation = tok.getVector3f()

            node.keyframes.append(keyframe)
        key.nodes.append(node)


def load(filePath) -> Key:
    f = open(filePath, 'r')
    tok = Tokenizer(f)
    key = Key(os.path.basename(filePath))

    while True:
        _skip_to_next_key_section(tok)
        t = tok.getToken()
        if t.type == TokenType.EOF:
            break

        if t.value.upper() == "HEADER":
            _parse_key_section_header(tok, key)

        elif t.value.upper() == "MARKERS":
            _parse_key_section_markers(tok, key)

        elif t.value.upper() == "KEYFRAME":
            tok.assertIdentifier("NODES")
            _parse_key_section_keyframe_nodes(tok, key)

    return key