import {
  Avatar,
  Button,
  Column,
  Heading,
  Icon,
  IconButton,
  Tag,
  Text,
  Meta,
  Schema,
  Row,
  Line,
} from "@once-ui-system/core";
import { baseURL, about, person, social } from "@/resources";
import React from "react";

export async function generateMetadata() {
  return Meta.generate({
    title: about.title,
    description: about.description,
    baseURL: baseURL,
    image: `/api/og/generate?title=${encodeURIComponent(about.title)}`,
    path: about.path,
  });
}

export default function About() {
  return (
    <Column maxWidth="s" gap="xl" paddingY="12" horizontal="center">
      <Schema
        as="webPage"
        baseURL={baseURL}
        title={about.title}
        description={about.description}
        path={about.path}
        image={`/api/og/generate?title=${encodeURIComponent(about.title)}`}
        author={{
          name: person.name,
          url: `${baseURL}${about.path}`,
          image: `${baseURL}${person.avatar}`,
        }}
      />

      {/* Header */}
      <Column fillWidth horizontal="center" align="center" gap="m">
        {about.avatar.display && <Avatar src={person.avatar} size="xl" />}
        <Column horizontal="center" align="center" gap="8">
          <Heading variant="display-strong-l">{person.name}</Heading>
          <Text variant="heading-default-m" onBackground="neutral-weak">
            {person.role}
          </Text>
          <Row gap="8" vertical="center" marginTop="4">
            <Icon onBackground="accent-weak" name="globe" size="s" />
            <Text variant="body-default-s" onBackground="neutral-weak">
              {person.location}
            </Text>
          </Row>
        </Column>

        {person.languages && person.languages.length > 0 && (
          <Row wrap gap="8" horizontal="center">
            {person.languages.map((language) => (
              <Tag key={language} size="l">{language}</Tag>
            ))}
          </Row>
        )}

        {social.length > 0 && (
          <Row wrap gap="8" horizontal="center" paddingTop="4">
            {social.map(
              (item) =>
                item.link && (
                  <React.Fragment key={item.name}>
                    <Row s={{ hide: true }}>
                      <Button
                        href={item.link}
                        prefixIcon={item.icon}
                        label={item.name}
                        size="s"
                        weight="default"
                        variant="secondary"
                      />
                    </Row>
                    <Row hide s={{ hide: false }}>
                      <IconButton
                        size="l"
                        href={item.link}
                        icon={item.icon}
                        variant="secondary"
                      />
                    </Row>
                  </React.Fragment>
                ),
            )}
          </Row>
        )}

        {about.calendar.display && (
          <Row
            fitWidth
            border="brand-alpha-medium"
            background="brand-alpha-weak"
            radius="full"
            padding="4"
            gap="8"
            vertical="center"
            style={{ backdropFilter: "blur(var(--static-space-1))" }}
          >
            <Icon paddingLeft="12" name="calendar" onBackground="brand-weak" />
            <Row paddingX="8">Schedule a call</Row>
            <IconButton
              href={about.calendar.link}
              data-border="rounded"
              variant="secondary"
              icon="chevronRight"
            />
          </Row>
        )}
      </Column>

      {/* Intro */}
      {about.intro.display && (
        <Column fillWidth gap="m">
          <Heading as="h2" variant="display-strong-s">{about.intro.title}</Heading>
          <Line />
          <Text variant="body-default-l">{about.intro.description}</Text>
        </Column>
      )}

      {/* Work Experience */}
      {about.work.display && (
        <Column fillWidth gap="l">
          <Heading as="h2" variant="display-strong-s">{about.work.title}</Heading>
          <Line />
          {about.work.experiences.map((experience, index) => (
            <Column key={`${experience.company}-${index}`} fillWidth gap="8">
              <Row fillWidth horizontal="between" vertical="end">
                <Text variant="heading-strong-l">{experience.company}</Text>
                <Text variant="heading-default-xs" onBackground="neutral-weak">
                  {experience.timeframe}
                </Text>
              </Row>
              <Text variant="body-default-s" onBackground="brand-weak" marginBottom="8">
                {experience.role}
              </Text>
              <Column as="ul" gap="12">
                {experience.achievements.map((achievement, achIndex) => (
                  <Text as="li" variant="body-default-m" key={`${experience.company}-${achIndex}`}>
                    {achievement}
                  </Text>
                ))}
              </Column>
            </Column>
          ))}
        </Column>
      )}

      {/* Studies */}
      {about.studies.display && (
        <Column fillWidth gap="l">
          <Heading as="h2" variant="display-strong-s">{about.studies.title}</Heading>
          <Line />
          {about.studies.institutions.map((institution, index) => (
            <Column key={`${institution.name}-${index}`} fillWidth gap="8">
              <Text variant="heading-strong-l">{institution.name}</Text>
              <Text variant="body-default-m" onBackground="neutral-weak">
                {institution.description}
              </Text>
            </Column>
          ))}
        </Column>
      )}

      {/* Technical Skills */}
      {about.technical.display && (
        <Column fillWidth gap="l">
          <Heading as="h2" variant="display-strong-s">{about.technical.title}</Heading>
          <Line />
          {about.technical.skills.map((skill, index) => (
            <Column key={`${skill.title}-${index}`} fillWidth gap="12">
              <Row fillWidth horizontal="between" vertical="end">
                <Text variant="heading-strong-m">{skill.title}</Text>
                <Text variant="heading-default-xs" onBackground="brand-weak">
                  {skill.description}
                </Text>
              </Row>
              <Row wrap gap="8">
                {skill.tags?.map((tag) => (
                  <Tag key={tag.name} size="l">{tag.name}</Tag>
                ))}
              </Row>
            </Column>
          ))}
        </Column>
      )}
    </Column>
  );
}
