import logo from './spotify.svg';
import './App.css';
import './index.css'
import Dictaphone from './Dictaphone';
import { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [song, setSong] = useState(null)
  const [artists, setArtists] = useState(null)
  const [album, setAlbum] = useState(null)
  const [emotion, setEmotion] = useState()

  useEffect(() => {
    if(song) {
      setAlbum(song.album)
      setArtists(song.artists)
    }
  }, [song])

  useEffect(() => {
    const res = getCurrentPlayingSong()
  }, [])
  
  const getCurrentPlayingSong = async () => {
    axios.get("http://localhost:8000/get_current_song").then((res) => {
      setSong(res.data['current-song'])
      console.log(res.data['current-song'])
    })
  }
  
  const playNextSong = async () => {
    axios.get("http://localhost:8000/play_next_song").then((res) => {
      setSong(res.data)
      console.log(res.data)
    })
  }
  
  const playPreviousSong = async () => {
    axios.get("http://localhost:8000/play_previous_song").then((res) => {
      setSong(res.data['current-song'])
      console.log(res.data['current-song'])
    })
  }


  return (
    <div className="App">
      <header className="App-header">
        <div className='flex flex-row align-middle items-center ml-36'>
          <h1 className=' text-6xl mt-2'>Spotter</h1>
          <img src={logo} className="App-logo" alt="logo" />
        </div>
        <div className=' bg-neutral-900 p-10 bg-opacity-60 rounded-3xl flex flex-col items-center shadow-lg'>
            <h2 className='mt-1 mb-4 text-4xl'> Current Emotion : {emotion}</h2>
            <div className='album-bar'>
              <button className='control-button bg-slate-50 text-lime-600 p-3 rounded-3xl text-xl' 
              onClick={(e) => playPreviousSong()}>Previous Song</button>
              {album? 
              <img src={album.images[0].url} className='album-cover rounded-3xl'></img>  :
              <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxISEhUSEhIVFRUVFRcVFRUVFRUVFRUVFRUWFhUVFRcYHSggGBolHRUVITEhJSkrLi4uFx8zODMtNygtLisBCgoKDQ0NFQ8PFSsZFRkrKy0tKystKy0tLTcrLS03Kzc3NzctNy0rLTc3Ky0tKy0tNy03LSstKzc3Kys3KystK//AABEIAOEA4QMBIgACEQEDEQH/xAAXAAEBAQEAAAAAAAAAAAAAAAAAAQIH/8QAIRABAQEAAQMEAwAAAAAAAAAAAAERAhJBYSFRgcExcZH/xAAWAQEBAQAAAAAAAAAAAAAAAAAAAQL/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwDjHJFrIwtQwAAwCFJSwAoaAICroQoiUWoKLEoCiVRCLqYoIFqgmDRYCasSEBQAZFoCCoCKUFChBAsABBRQwBEU5IKVYakBQAUgCBiKCwpEtAWJhoLoAIioChoCBTQFSU0A0KCEhgKuFNUEqRUwRTsiigEBYEBBABRFBUUBMirigxqKUBFNBDAAEUCIqUCACkUALUVKItpE1QBQCIuFBCRUwDVhIoGhFgJ6ewmUAKYgKIoM04qAkVNXAXfVmrCgkWIsAi1DQKi6gClBUrSSAiiys2gqKUBdSKBpI10saC9XITpAImELAIupCgBoCBiwEUSiippBFoSLgJiVUBYUBVAgglaqUEAgLixNJQXWbWoUGBcgCypYsSgAsoJA1KBqxFgBYSlAkWRCAsVKloGlQgKRMWAqxlQVKWmAFQBQoCynYwyggmAKcjQDBJTQIlVLAUhqQVrUAQwTVAikLQRFMAlNAFwNADQBCqAjUTAFRYgJn7DfM/gABQAgC4ixKCYupi4BIUKCLKmrBVgQETknZrEwEimLgGiLAWWz8fFQsATRQAgaBSkWAzgbQCKgBoACVaAi6igJY0yAsTFFUSKIlqpSgESLBVxYzFENBMAKFFVF0gipAwD4ABNKaAigC1FQEFpBQNNBFxFAwrTIgAAQkAUTGgQEwDAICwDAJAMAwXAGdDTQBFAotQEtVFopqVUtAWM41ADSFERUBVAtEXAAVE1rQZFAKSnIgLEqsgvUJgBS00AxUIC1ClgGiUwFpTS0ExqMxqAhVQE1YAARQSKLASItQBcRQCBgLqVUBBVBiQCgsAgFKuoCGlAABTFiKBEqlETBTBQhARaaRaCIuGgVNJVARQFRZUoG+RM8AIgA1AEFjPLsCi1IANcWQBeRQAKgC0AAAFigCU5gBx+z3AGYtAUAEABX/9k=" className='album-cover'></img>
              }
              <button className='control-button bg-slate-50 text-lime-600 p-3 rounded-3xl text-xl' 
              onClick={(e) => playNextSong()}>Next Song</button>
          </div>
          <h2 className='text-xl mt-5'>Currently playing:</h2>
          <p className='text-5xl mt-2 mb-2'>{song? song.name: "Nothing"}</p>
          <p>{artists? artists.map((artist, key) => {
            if (artists.length > 1 && key != (artists.length - 1)) {
              return `${artist.name}, `
            } else {
              return artist.name
            }
          }): ""}</p>
        </div>
        <Dictaphone setSong={setSong} setEmotion={setEmotion}/>
      </header>
    </div>
  );
}

export default App;
