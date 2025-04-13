// src/hooks/useRepos.js
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const fetchRepos = async (token) => {
  const { data } = await axios.get('https://api.github.com/user/repos', {
    headers: { Authorization: `token ${token}` },
  });
  return data;
};

export const useRepos = (token) => {
  return useQuery(['repos', token], () => fetchRepos(token), {
    enabled: !!token, // Only run the query if token exists
  });
};
