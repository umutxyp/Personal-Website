"use client";

import Image from "next/image";
import {
  Column,
  Flex,
  Heading,
  SmartLink,
  Text,
} from "@once-ui-system/core";

interface ProjectCardProps {
  href: string;
  priority?: boolean;
  images: string[];
  title: string;
  content: string;
  description: string;
  avatars: { src: string }[];
  link: string;
}

export const ProjectCard: React.FC<ProjectCardProps> = ({
  href,
  priority,
  images = [],
  title,
  content,
  description,
  avatars,
  link,
}) => {
  return (
    <Flex
      fillWidth
      radius="l"
      border="neutral-alpha-weak"
      overflow="hidden"
      s={{ direction: "column" }}
    >
      {images[0] && (
        <div style={{ width: "280px", flexShrink: 0, position: "relative", aspectRatio: "4/3" }}
          className="project-card-image">
          <Image
            priority={priority}
            src={images[0]}
            alt={title}
            fill
            style={{ objectFit: "cover" }}
          />
        </div>
      )}
      <Column flex={1} gap="12" padding="20" vertical="center">
        {title && (
          <Heading as="h2" wrap="balance" variant="heading-strong-m">
            {title}
          </Heading>
        )}
        {description?.trim() && (
          <Text wrap="balance" variant="body-default-s" onBackground="neutral-weak">
            {description}
          </Text>
        )}
        <Flex gap="16" wrap>
          {content?.trim() && (
            <SmartLink
              suffixIcon="arrowRight"
              style={{ margin: "0", width: "fit-content" }}
              href={href}
            >
              <Text variant="body-default-s">Read case study</Text>
            </SmartLink>
          )}
          {link && (
            <SmartLink
              suffixIcon="arrowUpRightFromSquare"
              style={{ margin: "0", width: "fit-content" }}
              href={link}
            >
              <Text variant="body-default-s">View project</Text>
            </SmartLink>
          )}
        </Flex>
      </Column>
    </Flex>
  );
};
