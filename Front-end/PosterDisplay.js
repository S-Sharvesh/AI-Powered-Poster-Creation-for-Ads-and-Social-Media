import React from 'react';

const PosterDisplay = ({ htmlContent }) => {
  return (
    <iframe
      srcDoc={htmlContent}
      title="Poster Display"
      style={{ width: '100%', height: '500px', border: 'none' }}
    ></iframe>
  );
};

export default PosterDisplay;
