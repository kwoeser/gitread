import React from 'react';
import './CustomizeReadme.css';

function CustomizeReadme({
  sections,
  setSections,
  styling,
  setStyling,
}) {
  // Toggle a boolean section (e.g. Overview, Quickstart)
  const handleToggleSection = (sectionKey) => {
    setSections((prev) => ({
      ...prev,
      [sectionKey]: !prev[sectionKey],
    }));
  };

  // Toggle a boolean styling option (e.g. generateLogo, addEmojis)
  const handleToggleStyling = (stylingKey) => {
    setStyling((prev) => ({
      ...prev,
      [stylingKey]: !prev[stylingKey],
    }));
  };

  return (
    <div className="customize-panel">
      <h2>Customize README</h2>
      <p className="panel-subtitle">Default Sections</p>

      <div className="sections-list">
        <label>
          <input
            type="checkbox"
            checked={sections.overview}
            onChange={() => handleToggleSection('overview')}
          />
          Overview
        </label>
        <label>
          <input
            type="checkbox"
            checked={sections.tableOfContents}
            onChange={() => handleToggleSection('tableOfContents')}
          />
          Table of Contents
        </label>
        <label>
          <input
            type="checkbox"
            checked={sections.quickstart}
            onChange={() => handleToggleSection('quickstart')}
          />
          Quickstart
        </label>
      </div>

      <p className="panel-subtitle">Styling</p>
      <div className="styling-options">
        <div className="option-group">
          <label>Header Alignment:</label>
          <div>
            <label>
              <input
                type="radio"
                name="headerAlignment"
                value="left"
                checked={styling.headerAlignment === 'left'}
                onChange={(e) =>
                  setStyling((prev) => ({ ...prev, headerAlignment: e.target.value }))
                }
              />
              Left
            </label>
            <label>
              <input
                type="radio"
                name="headerAlignment"
                value="center"
                checked={styling.headerAlignment === 'center'}
                onChange={(e) =>
                  setStyling((prev) => ({ ...prev, headerAlignment: e.target.value }))
                }
              />
              Center
            </label>
            <label>
              <input
                type="radio"
                name="headerAlignment"
                value="right"
                checked={styling.headerAlignment === 'right'}
                onChange={(e) =>
                  setStyling((prev) => ({ ...prev, headerAlignment: e.target.value }))
                }
              />
              Right
            </label>
          </div>
        </div>

        <div className="option-group">
          <label>Table of Contents Style:</label>
          <select
            value={styling.tableOfContentsStyle}
            onChange={(e) =>
              setStyling((prev) => ({ ...prev, tableOfContentsStyle: e.target.value }))
            }
          >
            <option value="bullets">Bullets</option>
            <option value="numbers">Numbers</option>
          </select>
        </div>

        <div className="option-group">
          <label>
            <input
              type="checkbox"
              checked={styling.generateLogo}
              onChange={() => handleToggleStyling('generateLogo')}
            />
            Generate Logo
          </label>
        </div>

        <div className="option-group">
          <label>
            <input
              type="checkbox"
              checked={styling.addEmojis}
              onChange={() => handleToggleStyling('addEmojis')}
            />
            Add Emojis to Headings
          </label>
        </div>
      </div>
    </div>
  );
}

export default CustomizeReadme;
