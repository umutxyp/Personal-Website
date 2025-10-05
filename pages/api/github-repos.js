export default async function handler(req, res) {
  try {
    const username = 'umutxyp'; // GitHub kullanıcı adınız
    
    // GitHub API'den public repos çek
    const response = await fetch(
      `https://api.github.com/users/${username}/repos?sort=updated&per_page=100`,
      {
        headers: {
          'Accept': 'application/vnd.github.v3+json',
          // GitHub token kullanmak isterseniz (rate limit artırır):
          // 'Authorization': `token ${process.env.GITHUB_TOKEN}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error('GitHub API request failed');
    }

    const repos = await response.json();

    // Sadece önemli bilgileri al ve yıldıza göre sırala
    const processedRepos = repos
      .filter(repo => !repo.fork && !repo.archived) // Fork'ları ve arşivlenmiş repoları hariç tut
      .map(repo => ({
        id: repo.id,
        name: repo.name,
        fullName: repo.full_name,
        description: repo.description || 'No description provided',
        // GitHub'ın otomatik oluşturduğu OpenGraph preview image
        image: `https://opengraph.githubassets.com/1/${repo.full_name}`,
        stars: repo.stargazers_count,
        forks: repo.forks_count,
        watchers: repo.watchers_count,
        language: repo.language,
        url: repo.html_url,
        homepage: repo.homepage,
        // Topics'leri gösterme, sadece dili kullan
        topics: [], // Boş array, sadece language kullanacağız
        createdAt: repo.created_at,
        updatedAt: repo.updated_at,
        isPrivate: repo.private,
      }))
      .sort((a, b) => b.stars - a.stars); // Yıldıza göre sırala

    // Cache header ekle (10 dakika)
    res.setHeader('Cache-Control', 's-maxage=600, stale-while-revalidate');
    
    res.status(200).json(processedRepos);
  } catch (error) {
    console.error('GitHub API Error:', error);
    res.status(500).json({ error: 'Failed to fetch GitHub repositories' });
  }
}
