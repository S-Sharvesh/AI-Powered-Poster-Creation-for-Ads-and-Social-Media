import React, { useState } from 'react';
import ReactQuill, { Quill } from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import './Editor.css';

// Add custom image handler
const CustomImage = () => {
  const input = document.createElement('input');
  input.setAttribute('type', 'file');
  input.setAttribute('accept', 'image/*');
  input.click();

  input.onchange = () => {
    const file = input.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      const range = this.quill.getSelection();
      this.quill.insertEmbed(range.index, 'image', e.target.result);
    };
    reader.readAsDataURL(file);
  };
};

// Add the custom handler to the toolbar
const modules = {
  toolbar: {
    container: [
      [{ 'header': '1'}, {'header': '2'}, { 'font': [] }],
      [{size: []}],
      ['bold', 'italic', 'underline', 'strike', 'blockquote'],
      [{'list': 'ordered'}, {'list': 'bullet'}, {'indent': '-1'}, {'indent': '+1'}],
      ['link', 'image'],
      ['clean']
    ],
    handlers: {
      'image': CustomImage,
    }
  },
  clipboard: {
    matchVisual: false,
  }
};

const Editor = ({ initialHtml, onSave }) => {
  const [html, setHtml] = useState(initialHtml);

  const handleSave = () => {
    onSave(html);
  };

  return (
    <div className="editor-container">
      <ReactQuill value={html} onChange={setHtml} modules={modules} />
      <button onClick={handleSave}>Save</button>
    </div>
  );
};

export default Editor;
