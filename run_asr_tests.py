import os
import glob
import wave
import json
import whisper
# from vosk import Model, KaldiRecognizer

def transcribe_whisper(audio_file, model_path):
    print(f"Starting Whisper Transcription with model: {model_path} for file: {audio_file}")
    model = whisper.load_model(model_path)
    result = model.transcribe(audio_file)  # Use the audio_file parameter here
    return result['text']

def transcribe_vosk(audio_file, model_path):
    print(f"Starting Vosk Transcription with model: {model_path} for file: {audio_file}")
    model = Model(model_path)
    rec = KaldiRecognizer(model, 16000)
    
    with wave.open(audio_file, "rb") as wf:
        rec.AcceptWaveform(wf.readframes(wf.getnframes()))
    result = json.loads(rec.Result())
    return result.get('text', '')

def transcribe_julius(audio_file, model_path):
    # Placeholder function for Julius ASR
    # Replace with actual implementation
    return "Julius ASR result placeholder"

def transcribe_sense_voice(audio_file, model_path):
    # Placeholder function for Sense Voice ASR
    # Replace with actual implementation
    return "Sense Voice ASR result placeholder"

def process_folder(folder_path):
    asr_models = {
        'whisper-tiny.en': 'tiny.en',
        'whisper-small': 'small',
        'whisper-tiny': 'tiny',
        'whisper-base': 'base',
        'whisper-large-v2': 'large-v2',
        'whisper-large-v3': 'large-v3',
        # 'vosk': '/path/to/vosk/model',
        # 'julius': '/path/to/julius/model',
        # 'sense-voice': '/path/to/sense-voice/model'
    }

    for lang_folder in os.listdir(folder_path):
        lang_path = os.path.join(folder_path, lang_folder)
        if not os.path.isdir(lang_path):
            continue

        for audio_file in glob.glob(os.path.join(lang_path, '*')):
            testcase_name = os.path.splitext(os.path.basename(audio_file))[0]

            for model_name, model_path in asr_models.items():
                if 'whisper' in model_name:
                    transcript = transcribe_whisper(audio_file, model_path)
                elif model_name == 'vosk':
                    transcript = transcribe_vosk(audio_file, model_path)
                elif model_name == 'julius':
                    transcript = transcribe_julius(audio_file, model_path)
                elif model_name == 'sense-voice':
                    transcript = transcribe_sense_voice(audio_file, model_path)
                else:
                    transcript = "Model not implemented"

                output_folder = f'asr_result_lang_{lang_folder}'
                os.makedirs(output_folder, exist_ok=True)

                output_file = os.path.join(output_folder, f'case_{testcase_name}_model_{model_name}.txt')
                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(transcript)

                print(f"Transcription saved to {output_file}")
    # 计算错词率
    subprocess.run(['python', 'run_wer_results.py'])


# Usage example
process_folder('test_data')
