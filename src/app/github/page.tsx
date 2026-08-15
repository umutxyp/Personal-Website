import type { Metadata } from "next";
import {
  Badge,
  Card,
  Column,
  Heading,
  Row,
  Schema,
  Text,
} from "@once-ui-system/core";
import { baseURL, person, about, siteData } from "@/resources";

type GitHubRepo = {
  id: number;
  name: string;
  html_url: string;
  description: string | null;
  stargazers_count: number;
  forks_count: number;
  language: string | null;
  updated_at: string;
};

async function fetchRepos(): Promise<GitHubRepo[]> {
  try {
    const response = await fetch(
      `https://api.github.com/users/${siteData.github.username}/repos?per_page=100&sort=updated`,
      {
        headers: {
          Accept: "application/vnd.github+json",
          "User-Agent": "portfolio-app",
        },
        next: { revalidate: 60 * 60 },
      },
    );

    if (!response.ok) {
      console.warn("Failed to load GitHub repositories", await response.text());
      return [];
    }

    const json = (await response.json()) as GitHubRepo[];
    return json;
  } catch (error) {
    console.error("Error fetching GitHub repositories", error);
    return [];
  }
}

/**
 * The pinned repositories are whatever is pinned on the GitHub profile itself.
 * The REST API does not expose pins and the GraphQL API needs a token, so the
 * public profile page is the source of truth — repin on GitHub and this follows.
 * Falls back to the hardcoded list if the scrape ever comes back empty.
 */
async function fetchPinnedNames(): Promise<string[]> {
  try {
    const response = await fetch(`https://github.com/${siteData.github.username}`, {
      headers: {
        Accept: "text/html",
        "User-Agent": "portfolio-app",
      },
      next: { revalidate: 60 * 60 },
    });

    if (!response.ok) return siteData.github.highlight;

    const html = await response.text();
    const names = [...html.matchAll(/class="repo"[^>]*>([^<]+)</g)].map((match) =>
      match[1].trim(),
    );

    const unique = [...new Set(names)];
    return unique.length > 0 ? unique : siteData.github.highlight;
  } catch (error) {
    console.error("Error fetching pinned repositories", error);
    return siteData.github.highlight;
  }
}

export const metadata: Metadata = {
  title: `GitHub Projects - ${person.name}`,
  description: siteData.github.description,
};

function RepoCard({ repo, pinned }: { repo: GitHubRepo; pinned?: boolean }) {
  return (
    <Card
      href={repo.html_url}
      border={pinned ? "brand-alpha-weak" : "neutral-alpha-weak"}
      padding="l"
      radius="l"
      background="surface"
      shadow={pinned ? "m" : undefined}
      fillWidth
      fillHeight
      direction="column"
    >
      <Column gap="12" fillWidth fillHeight vertical="between">
        <Column gap="8" fillWidth>
          <Row gap="8" vertical="center" wrap>
            <Heading
              as="h3"
              variant="heading-strong-s"
              style={{
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
                maxWidth: "100%",
              }}
            >
              {repo.name}
            </Heading>
            {pinned && (
              <Badge
                background="brand-alpha-weak"
                paddingX="8"
                paddingY="2"
                textVariant="label-default-xs"
              >
                Pinned
              </Badge>
            )}
          </Row>
          <Text
            onBackground="neutral-weak"
            variant="body-default-s"
            style={{
              display: "-webkit-box",
              WebkitLineClamp: 3,
              WebkitBoxOrient: "vertical",
              overflow: "hidden",
              textOverflow: "ellipsis",
            }}
          >
            {repo.description || "This project ships without a description yet."}
          </Text>
        </Column>
        <Row gap="16" vertical="center" wrap>
          {repo.language && (
            <Text variant="label-default-s" onBackground="neutral-medium">
              {repo.language}
            </Text>
          )}
          <Text variant="label-default-s" onBackground="neutral-medium">
            ⭐ {repo.stargazers_count}
          </Text>
          <Text variant="label-default-s" onBackground="neutral-medium">
            🍴 {repo.forks_count}
          </Text>
          <Text variant="label-default-xs" onBackground="neutral-weak">
            Updated {new Date(repo.updated_at).toLocaleDateString()}
          </Text>
        </Row>
      </Column>
    </Card>
  );
}

export default async function GitHubPage() {
  const [repos, pinnedNames] = await Promise.all([fetchRepos(), fetchPinnedNames()]);

  const byLowerName = new Map(repos.map((repo) => [repo.name.toLowerCase(), repo]));

  // Keep the order GitHub shows them in, and drop pins we cannot resolve
  // (an org-owned pin will not appear in this user's repository list).
  const highlighted = pinnedNames
    .map((name) => byLowerName.get(name.toLowerCase()))
    .filter((repo): repo is GitHubRepo => Boolean(repo));

  // Everything that is not pinned, most-starred first — a repository people
  // actually use should not sit below one that was merely touched more recently.
  const highlightedIds = new Set(highlighted.map((repo) => repo.id));
  const others = repos
    .filter((repo) => !highlightedIds.has(repo.id))
    .sort((a, b) => b.stargazers_count - a.stargazers_count);

  return (
    <Column maxWidth="m" paddingTop="24" gap="xl">
      <Schema
        as="webPage"
        baseURL={baseURL}
        path="/github"
        title="GitHub Projects"
        description={siteData.github.description}
        image={`/api/og/generate?title=${encodeURIComponent(`GitHub Projects - ${person.name}`)}`}
        author={{
          name: person.name,
          url: `${baseURL}${about.path}`,
          image: `${baseURL}${person.avatar}`,
        }}
      />
      <Heading align="center" variant="heading-strong-xl">
        GitHub Projects
      </Heading>
      <Text align="center" onBackground="neutral-weak">
        {siteData.github.description}
      </Text>

      {highlighted.length > 0 && (
        <Column gap="m" fillWidth>
          <Heading variant="heading-strong-m">Pinned work</Heading>
          <div className="repo-grid">
            {highlighted.map((repo) => (
              <RepoCard key={repo.id} repo={repo} pinned />
            ))}
          </div>
        </Column>
      )}

      <Column gap="m" fillWidth>
        <Heading variant="heading-strong-m">Other repositories</Heading>
        {others.length === 0 && (
          <Text onBackground="neutral-weak">
            GitHub rate limits prevented loading repositories. Try again in a few minutes.
          </Text>
        )}
        <div className="repo-grid">
          {others.map((repo) => (
            <RepoCard key={repo.id} repo={repo} />
          ))}
        </div>
      </Column>
    </Column>
  );
}
