import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

const fetchRepos = async (token) => {
  if (!token) {
    throw new Error("GitHub token is required");
  }
  const { data } = await axios.get('https://api.github.com/user/repos', {
    headers: { Authorization: `token ${token}` },
  });
  return data;
};

function App() {
  const [githubToken, setGithubToken] = useState('');
  const [selectedRepo, setSelectedRepo] = useState(null);
  const [readme, setReadme] = useState('');
  const [loadingGenerate, setLoadingGenerate] = useState(false);

  // Your React Query hook for fetching repos (update to v5 syntax)
  const { data: repos, error, isLoading } = useQuery({
    queryKey: ['repos', githubToken],
    queryFn: () => fetchRepos(githubToken),
    enabled: Boolean(githubToken),
  });

  const handleGenerateReadme = async () => {
    if (!selectedRepo) return;
    setLoadingGenerate(true);
    try {
      const response = await axios.post('/generate_readme_from_repo', {
        repo_url: selectedRepo.html_url,
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
    <div style={{ padding: '20px' }}>
      <h1>GitHub README Generator</h1>
      <div>
        <input
          type="text"
          placeholder="Enter GitHub token"
          value={githubToken}
          onChange={(e) => setGithubToken(e.target.value)}
          style={{ width: '300px', marginRight: '10px' }}
        />
      </div>
      {isLoading && <p>Loading repositories...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error.message}</p>}
      {repos && repos.length > 0 && (
        <div>
          <h2>Your Repositories</h2>
          <ul>
            {repos.map((repo) => (
              <li
                key={repo.id}
                onClick={() => setSelectedRepo(repo)}
                style={{
                  cursor: 'pointer',
                  margin: '5px 0',
                  fontWeight: selectedRepo?.id === repo.id ? 'bold' : 'normal',
                }}
              >
                {repo.full_name}
              </li>
            ))}
          </ul>
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
      {readme && (
        <div style={{ marginTop: '20px' }}>
          <h2>Generated README</h2>
          <div style={{ background: '#f4f4f4', padding: '10px', borderRadius: '5px' }}>
            <ReactMarkdown>{readme}</ReactMarkdown>
          </div>
          <a href="/download_readme" target="_blank" rel="noopener noreferrer">
            <button>Download README</button>
          </a>
        </div>
      )}
    </div>
  );
}

export default App;