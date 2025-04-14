import React from 'react';
import './CustomizeReadme.css';

function CustomizeReadme({ sections, setSections, styling, setStyling }) {
  const toggleSection = (key) => {
    setSections(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleStylingChange = (key, value) => {
    setStyling(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="customize-panel">
      <h2>Customize Your README</h2>
      <div className="customize-section">
        <p>Extra Sections to include:</p>
        <div className="checkbox-group">
          <label>
            <input
              type="checkbox"
              checked={sections.overview}
              onChange={() => toggleSection('overview')}
            />
            Overview
          </label>
          <label>
            <input
              type="checkbox"
              checked={sections.tableOfContents}
              onChange={() => toggleSection('tableOfContents')}
            />
            Table of Contents
          </label>
          <label>
            <input
              type="checkbox"
              checked={sections.quickstart}
              onChange={() => toggleSection('quickstart')}
            />
            Quickstart
          </label>
        </div>
      </div>
      <div className="customize-styling">
        <p>Styling options:</p>
        <div className="option-group">
          <label>Header Alignment:</label>
          <select
            value={styling.headerAlignment}
            onChange={(e) => handleStylingChange('headerAlignment', e.target.value)}
          >
            <option value="left">Left</option>
            <option value="center">Center</option>
            <option value="right">Right</option>
          </select>
        </div>
        {sections.tableOfContents && (
          <div className="option-group">
            <label>TOC Style:</label>
            <select
              value={styling.tableOfContentsStyle}
              onChange={(e) => handleStylingChange('tableOfContentsStyle', e.target.value)}
            >
              <option value="bullets">Bullets</option>
              <option value="numbers">Numbers</option>
            </select>
          </div>
        )}
        <div className="option-group">
          <label>
            <input
              type="checkbox"
              checked={styling.addEmojis}
              onChange={() => handleStylingChange('addEmojis', !styling.addEmojis)}
            />
            Add Emojis to Headings
          </label>
        </div>
      </div>
    </div>
  );
}

export default CustomizeReadme;
