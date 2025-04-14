import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw'; 
import CustomizeReadme from './CustomizeReadme';
import './index.css';

axios.defaults.withCredentials = true;

// Use the VITE_API_URL environment variable or fallback to localhost.
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const fetchRepos = async () => {
  const { data } = await axios.get(`${API_URL}/repos`);
  return data;
};

function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [selectedRepo, setSelectedRepo] = useState(null);
  const [readme, setReadme] = useState('');
  const [loadingGenerate, setLoadingGenerate] = useState(false);

  // State for custom settings
  const [sections, setSections] = useState({
    overview: true,
    tableOfContents: true,
    quickstart: true,
  });
  const [styling, setStyling] = useState({
    headerAlignment: 'left',
    tableOfContentsStyle: 'bullets',
    addEmojis: false,
  });

  useEffect(() => {
    axios.get(`${API_URL}/auth/status`)
      .then(response => setIsConnected(response.data.connected))
      .catch(() => setIsConnected(false));
  }, []);

  // Fetch repositories only if connected.
  const { data: repos, error, isLoading } = useQuery({
    queryKey: ['repos'],
    queryFn: fetchRepos,
    enabled: isConnected,
  });

  const handleLogin = () => {
    window.location.href = `${API_URL}/login/github`;
  };

  const handleLogout = () => {
    window.location.href = `${API_URL}/logout`;
  };

  const handleGenerateReadme = async () => {
    if (!selectedRepo) return;
    console.log('Custom sections:', sections);
    console.log('Custom styling:', styling);
    setLoadingGenerate(true);
    try {
      const response = await axios.post(`${API_URL}/generate_readme_from_repo`, {
        repo_url: selectedRepo.html_url,
        sections,
        styling,
      });
      setReadme(response.data.README);
    } catch (err) {
      console.error('Error generating README:', err);
      alert("Error generating README");
    } finally {
      setLoadingGenerate(false);
    }
  };

  return (
    <div className="container">
      <h1>GitHub README Generator</h1>
      <p>Automatically generate detailed template README files based on your repos.</p>
      {!isConnected ? (
        <button onClick={handleLogin}>Connect to GitHub</button>
      ) : (
        <button onClick={handleLogout}>Disconnect from GitHub</button>
      )}

      {isConnected && (
        <div className="layout">
          {/* Left Panel: Customization */}
          <div className="left-panel">
            <CustomizeReadme
              sections={sections}
              setSections={setSections}
              styling={styling}
              setStyling={setStyling}
            />
          </div>

          {/* Right Panel: Repo Selection and README Preview */}
          <div className="right-panel">
            {isLoading && <p>Loading repositories...</p>}
            {error && <p className="error">Error: {error.message}</p>}
            {repos && repos.length > 0 && (
              <div className="repo-selection">
                <h2>Select a Repository</h2>
                <select
                  onChange={(e) => {
                    const repo = repos.find(r => r.id === Number(e.target.value));
                    setSelectedRepo(repo);
                  }}
                  defaultValue=""
                >
                  <option value="" disabled>
                    -- Select Repository --
                  </option>
                  {repos.map((repo) => (
                    <option key={repo.id} value={repo.id}>
                      {repo.full_name}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {selectedRepo && (
              <div className="generate-section">
                <h3>Selected Repository: {selectedRepo.full_name}</h3>
                <button onClick={handleGenerateReadme} disabled={loadingGenerate}>
                  {loadingGenerate ? 'Generating README...' : 'Generate README'}
                </button>
              </div>
            )}

            {readme && (
              <div className="readme-section">
                <div className="readme-header">
                  <h2>Generated README</h2>
                  <a
                    href={`${API_URL}/download_readme`}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <button className="download-button">Download README</button>
                  </a>
                </div>
                <p className="regenerate-info">
                  If you don't like the current rendition of the README, click the "Generate README" again.
                  <br></br>Also will most likely need to change some specifics about the README.
                </p>
                <div className="markdown-container">
                  <ReactMarkdown rehypePlugins={[rehypeRaw]}>
                    {readme}
                  </ReactMarkdown>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
