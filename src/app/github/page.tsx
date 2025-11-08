import type { Metadata } from "next";
import {
  Badge,
  Card,
  Column,
  Grid,
  Heading,
  Meta,
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

export const metadata: Metadata = {
  title: `GitHub Projects - ${person.name}`,
  description: siteData.github.description,
};

export default async function GitHubPage() {
  const repos = await fetchRepos();
  const highlightNames = new Set(
    siteData.github.highlight.map((name) => name.toLowerCase()),
  );

  const highlighted = repos.filter((repo) => highlightNames.has(repo.name.toLowerCase()));
  const others = repos.filter((repo) => !highlightNames.has(repo.name.toLowerCase()));

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
        <Column gap="m">
          <Heading variant="heading-strong-m">Pinned work</Heading>
          <Grid columns="2" s={{ columns: 1 }} gap="16">
            {highlighted.map((repo) => (
              <Card
                key={repo.id}
                href={repo.html_url}
                border="brand-alpha-weak"
                padding="l"
                radius="l"
                background="surface"
                shadow="m"
                fillWidth
                style={{ minHeight: '200px' }}
              >
                <Column gap="8" fillHeight vertical="between">
                  <Column gap="8">
                    <Row gap="12" vertical="center">
                      <Heading as="h3" variant="heading-strong-s">
                        {repo.name}
                      </Heading>
                      <Badge
                        background="brand-alpha-weak"
                        paddingX="8"
                        paddingY="2"
                        textVariant="label-default-xs"
                      >
                        Pinned
                      </Badge>
                    </Row>
                    <Text 
                      onBackground="neutral-weak"
                      style={{
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                      }}
                    >
                      {repo.description || "This project ships without a description yet."}
                    </Text>
                  </Column>
                  <Row gap="16" vertical="center">
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
            ))}
          </Grid>
        </Column>
      )}

      <Column gap="m">
        <Heading variant="heading-strong-m">Latest repositories</Heading>
        {others.length === 0 && (
          <Text onBackground="neutral-weak">
            GitHub rate limits prevented loading repositories. Try again in a few minutes.
          </Text>
        )}
        <Column gap="m">
          {others.map((repo) => (
            <Card
              key={repo.id}
              href={repo.html_url}
              border="neutral-alpha-weak"
              padding="m"
              radius="m"
              background="surface"
            >
              <Column gap="8">
                <Heading as="h3" variant="heading-strong-s">
                  {repo.name}
                </Heading>
                <Text onBackground="neutral-weak">
                  {repo.description || "This project ships without a description yet."}
                </Text>
                <Row gap="16" vertical="center">
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
          ))}
        </Column>
      </Column>
    </Column>
  );
}
