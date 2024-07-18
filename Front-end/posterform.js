import React, { useState } from 'react';

function PosterForm({ onGenerate }) {
  const [formData, setFormData] = useState({
    topic: '',
    background_color: '',
    template_color: '',
    font_color: '',
    background_image_url: '',
    logo_url: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onGenerate(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>Topic: <input className="input-field" type="text" name="topic" value={formData.topic} onChange={handleChange} /></label><br/>
      <label>Background Color: <input type="color" name="background_color" value={formData.background_color} onChange={handleChange}autoComplete /></label><br/>
      <label>Template Color: <input type="color" name="template_color" value={formData.template_color} onChange={handleChange} /></label><br/>
      <label>Font Color: <input type="color" name="font_color" value={formData.font_color} onChange={handleChange} /></label><br/>
      <label>Background Image URL: <input type="text" name="background_image_url" value={formData.background_image_url} onChange={handleChange} /></label><br/>
      <label>Logo URL: <input type="text" name="logo_url" value={formData.logo_url} onChange={handleChange} /></label><br/>
      <button type="submit">Generate Poster</button><br/>
    </form>
  );
}

export default PosterForm;
