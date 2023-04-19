import React from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import axios from 'axios'
import { useState, useEffect } from 'react';

const Dictaphone = ({setSong, setEmotion}) => {
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition
  } = useSpeechRecognition();

  const [currentText, setCurrentText] = useState(transcript)

  useEffect(() => {
    setCurrentText(transcript)
  }, [transcript])

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }

  function toTitleCase(str) {
    return str.replace(
      /\w\S*/g,
      function(txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
      }
    );
  }

  const handleTextSubmission = () => {
    const text= transcript;

    resetTranscript()
    const res = analysisText(text)
    setTimeout(() => {
      setCurrentText(null);
    }, 2000)

  }

  const analysisText = async (text) => {
    axios.post("http://localhost:8000/analyse_audio", {
      'text':text
    }).then((res) => {
      console.log(res)
      const data = res.data
      setSong(data)
      setEmotion(toTitleCase(data.emotion))
    })
  }

  return (
    <div>
      <button className='control-button bg-slate-50 text-red-600 p-3 rounded-3xl text-2xl mt-10' 
      onClick={SpeechRecognition.startListening}>{listening? "Recording...": "Record"}</button>
      {currentText?
      <p className='text-4xl text-green-600 mt-5 bg-neutral-900 bg-opacity-75 p-3 rounded-lg'>{currentText}</p>:
      ""
    }
      {(!listening && transcript)? handleTextSubmission():""}
    </div>
  );
};
export default Dictaphone;