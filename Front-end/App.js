import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PosterForm from './components/posterform'; // Ensure your import paths are correct
import PosterDisplay from './components/PosterDisplay';
import Editor from './components/Editor';
import './App.css';

function App() {
  const [posterHtml, setPosterHtml] = useState('');
  const [allPosters, setAllPosters] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [editingHtml, setEditingHtml] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [selectedPosterId, setSelectedPosterId] = useState(null);

  useEffect(() => {
    fetchAllPosters();
  }, []);

  const fetchAllPosters = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/getposters');
      setAllPosters(response.data);
    } catch (err) {
      console.error('Failed to fetch posters:', err);
    }
  };

  const generatePoster = async (data) => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.post('http://127.0.0.1:5000/generateposter', data);
      setPosterHtml(response.data);
      fetchAllPosters(); // Refresh the list after generating a new poster
    } catch (err) {
      setError('Failed to generate poster.');
    } finally {
      setLoading(false);
    }
  };

  const handleEditPoster = (poster) => {
    setEditingHtml(poster.poster_html);
    setSelectedPosterId(poster.id);
    setIsEditing(true);
  };

  const handleSaveEditedPoster = async (html) => {
    if (selectedPosterId) {
      try {
        await axios.post(`http://127.0.0.1:5000/updateposter/${selectedPosterId}`, {
          poster_html: html,
        });
        setEditingHtml(html);
        setPosterHtml(html);
        setIsEditing(false);
        alert('Poster updated successfully!');
        fetchAllPosters(); // Refresh the list to reflect the changes
      } catch (err) {
        console.error('Error updating poster:', err);
        alert('Failed to update poster.');
      }
    }
  };

  const handleDownloadPoster = (html, id) => {
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `poster_${id}.html`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="App">
      <h1>Poster Generator</h1>
      <PosterForm onGenerate={generatePoster} />
      {loading && <p>Generating poster...</p>}
      {error && <p className="error">{error}</p>}
      {posterHtml && (
        <div>
          <h2>Generated Poster</h2>
          {isEditing ? (
            <Editor initialHtml={editingHtml} onSave={handleSaveEditedPoster} />
          ) : (
            <div>
              <PosterDisplay htmlContent={posterHtml.poster_html} />
              <button onClick={() => handleEditPoster({ id: posterHtml.id, poster_html: posterHtml.poster_html })}>Edit Poster</button>
              <button onClick={() => handleDownloadPoster(posterHtml.poster_html, posterHtml.id)}>Download Poster</button>
            </div>
          )}
        </div>
      )}
      <h2>All Posters</h2>
      <div className="all-posters">
        {allPosters.map((poster) => (
          <div key={poster.id}>
            <PosterDisplay htmlContent={poster.poster_html} />
            <button onClick={() => handleEditPoster(poster)}>Edit Poster</button>
            <button onClick={() => handleDownloadPoster(poster.poster_html, poster.id)}>Download Poster</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;