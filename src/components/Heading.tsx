import { Pic } from "./Pic";

/** A section's title, a pen stroke under it, and the theme's line running off to the right. */
export function Heading({ children, line = 0, id }: { children: string; line?: 0 | 1 | 2; id?: string }) {
  return (
    <div className="heading" id={id}>
      <h2 className="wavy">{children}</h2>
      <Pic name={`line-${line}`} width={900} height={84} />
    </div>
  );
}
