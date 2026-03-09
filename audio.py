import torch
import subprocess

# Work around Coqui TTS expecting `BeamSearchScorer` at the transformers root.
# Different transformers versions expose it in different modules, so we try a few.
try:
    import transformers as _transformers
    _BeamSearchScorer = None
    try:
        from transformers.generation import BeamSearchScorer as _BeamSearchScorer  # type: ignore[attr-defined]
    except Exception:
        try:
            from transformers.generation.beam_search import BeamSearchScorer as _BeamSearchScorer  # type: ignore[attr-defined]
        except Exception:
            try:
                from transformers.generation_beam_search import BeamSearchScorer as _BeamSearchScorer  # type: ignore[attr-defined]
            except Exception:
                try:
                    from transformers.generation_utils import BeamSearchScorer as _BeamSearchScorer  # type: ignore[attr-defined]
                except Exception:
                    _BeamSearchScorer = None

    if _BeamSearchScorer is not None and not hasattr(_transformers, "BeamSearchScorer"):
        setattr(_transformers, "BeamSearchScorer", _BeamSearchScorer)
except Exception:
    # If anything goes wrong here, we fall back and let TTS handle its own imports.
    pass

from TTS.api import TTS


### Leverage coqui TTS for text scraped to audio ==>
def audio(text_file_path, file_path="audio/output.wav", speaker_wav="assets/trump.mp3"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Read the text from the file
    with open(text_file_path, 'r', encoding='utf-8') as file:
        text = file.read().strip()
    # Init TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    tts.tts_to_file(text= text
                    , speaker_wav = speaker_wav, language="en", file_path=file_path)


## Converting audio to 16khz, 16 bit and mono so that we can represent them during force alignment
def convert_audio(input_path, output_path):
    command = [
        'ffmpeg',
        '-y',
        '-i', input_path,  # Input file
        '-ac', '1',  # Set number of audio channels to 1 (mono)
        '-ar', '16000',  # Set audio sampling rate to 16kHz
        '-sample_fmt', 's16',  # Set sample forymat to 16-bit
        output_path  # Output file
    ]
    subprocess.run(command, check=True)
    print("AUDIO CONVERSION DONE!")

