import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import CustomizeReadme from './CustomizeReadme';
import './index.css';

axios.defaults.withCredentials = true;

const fetchRepos = async () => {
  const { data } = await axios.get('http://localhost:5000/repos');
  return data;
};

function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [selectedRepo, setSelectedRepo] = useState(null);
  const [readme, setReadme] = useState('');
  const [loadingGenerate, setLoadingGenerate] = useState(false);

  // State for customizing the README
  const [sections, setSections] = useState({
    overview: true,
    tableOfContents: true,
    quickstart: true,
  });
  const [styling, setStyling] = useState({
    headerAlignment: 'left',
    tableOfContentsStyle: 'bullets',
    generateLogo: false,
    addEmojis: false,
  });

  // Check connection status on mount.
  useEffect(() => {
    axios.get('http://localhost:5000/auth/status')
      .then(response => {
        setIsConnected(response.data.connected);
      })
      .catch(() => setIsConnected(false));
  }, []);

  // Fetch repositories only if connected.
  const { data: repos, error, isLoading } = useQuery({
    queryKey: ['repos'],
    queryFn: fetchRepos,
    enabled: isConnected,
  });

  // Initiates the GitHub OAuth flow.
  const handleLogin = () => {
    window.location.href = 'http://localhost:5000/login/github';
  };

  // Logs out the user.
  const handleLogout = () => {
    window.location.href = 'http://localhost:5000/logout';
  };

  const handleGenerateReadme = async () => {
    if (!selectedRepo) return;

    // For demonstration, just logging the user’s choices:
    console.log('Selected sections:', sections);
    console.log('Styling options:', styling);

    setLoadingGenerate(true);
    try {
      const response = await axios.post('http://localhost:5000/generate_readme_from_repo', {
        repo_url: selectedRepo.html_url,
        // Optionally include sections/styling in your request body:
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
      <p>Automatically generate detailed README files based on your repos.</p>
      {!isConnected ? (
        <button onClick={handleLogin}>Connect with GitHub</button>
      ) : (
        <button onClick={handleLogout}>Disconnect from GitHub</button>
      )}

      {isConnected && (
        <>
          {/* The new customize panel */}
          <CustomizeReadme
            sections={sections}
            setSections={setSections}
            styling={styling}
            setStyling={setStyling}
          />

          {isLoading && <p>Loading repositories...</p>}
          {error && <p className="error">Error: {error.message}</p>}
          {repos && repos.length > 0 && (
            <div className="dropdown-container">
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
            <div>
              <h2>Selected Repository: {selectedRepo.full_name}</h2>
              <button onClick={handleGenerateReadme} disabled={loadingGenerate}>
                {loadingGenerate ? 'Generating README...' : 'Generate README'}
              </button>
            </div>
          )}
        </>
      )}

      {readme && (
        <div className="readme-section">
          <div className="readme-header">
            <h2>Generated README</h2>
            <a href="http://localhost:5000/download_readme" target="_blank" rel="noopener noreferrer">
              <button className="download-button">Download README</button>
            </a>
          </div>
          <div className="markdown-container">
            <ReactMarkdown>{readme}</ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
