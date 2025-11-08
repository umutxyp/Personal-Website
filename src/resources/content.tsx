import { Row, Line, Text } from "@once-ui-system/core";
import type { About, Blog, Gallery, Home, Newsletter, Person, Social, Work } from "@/types";
import siteData from "./site-data";
import React from "react";

const person: Person = {
  firstName: siteData.person.firstName,
  lastName: siteData.person.lastName,
  name: siteData.person.name,
  role: siteData.person.role,
  avatar: siteData.person.avatar,
  email: siteData.person.email,
  location: siteData.person.timezone as Person["location"],
  languages: siteData.person.languages,
};

const newsletter: Newsletter = {
  display: siteData.newsletter.display,
  title: <>{siteData.newsletter.title}</>,
  description: <>{siteData.newsletter.description}</>,
};

const social: Social = siteData.social;

const home: Home = {
  path: "/",
  image: "/images/og/home.jpg",
  label: "Home",
  title: `${person.name} | ${person.role}`,
  description: siteData.person.biography,
  headline: <>{siteData.hero.headline}</>,
  featured: {
    display: true,
    title: (
      <Row gap="12" vertical="center">
        <strong className="ml-4">{siteData.hero.featured.badge}</strong>{" "}
        <Line background="brand-alpha-strong" vert height="20" />
        <Text marginRight="4" onBackground="brand-medium">
          {siteData.hero.featured.label}
        </Text>
      </Row>
    ),
    href: siteData.hero.featured.href,
  },
  subline: siteData.hero.subline,
};

const about: About = {
  path: "/about",
  label: "About",
  title: `About - ${person.name}`,
  description: siteData.person.biography,
  tableOfContent: {
    display: true,
    subItems: false,
  },
  avatar: {
    display: true,
  },
  calendar: {
    display: false,
    link: "https://cal.com/umutxyp",
  },
  intro: {
    display: true,
    title: "Hello!",
    description: <>{siteData.about.introDescription}</>,
  },
  work: {
    display: true,
    title: "Work Experience",
    experiences: siteData.about.experiences.map((experience) => ({
      company: experience.company,
      timeframe: experience.timeframe,
      role: experience.role,
      achievements: experience.achievements.map((achievement, idx) => <React.Fragment key={`${experience.company}-${idx}`}>{achievement}</React.Fragment>),
      images: [],
    })),
  },
  studies: {
    display: true,
    title: "Studies",
    institutions: siteData.about.studies.map((study) => ({
      name: study.name,
      description: <>{study.description}</>,
    })),
  },
  technical: {
    display: true,
    title: "Technical focus",
    skills: siteData.about.technical.map((skill) => ({
      title: skill.title,
      description: <>{skill.description}</>,
      tags: skill.tags,
      images: [],
    })),
  },
};

const blog: Blog = {
  path: "/blog",
  label: "Blog",
  title: "Writing about code, community, and content",
  description: `Notes on CodeShare, creators, and automation experiments by ${person.name}`,
};

const work: Work = {
  path: "/work",
  label: "Work",
  title: `Projects - ${person.name}`,
  description: `Software, marketplaces, and community experiments by ${person.name}`,
};

const gallery: Gallery = {
  path: "/gallery",
  label: "Gallery",
  title: `Product gallery - ${person.name}`,
  description: "Screens from CodeShare, Beatra, Vip Transfer Turkey, and DNZ Geri Dönüşüm.",
  images: siteData.gallery.map((src, index) => ({
    src,
    alt: `showcase-${index + 1}`,
    orientation: index % 2 === 0 ? "horizontal" : "vertical",
  })),
};

export { person, social, newsletter, home, about, blog, work, gallery };
