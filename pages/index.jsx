import Head from 'next/head';
import Image from 'next/image';
import swr from '../lib/swr';

export default function Home() {
  const { data: _repositories } = swr("/api/repos");
  const repositories = _repositories ? _repositories : null;

  return (
    <>
      <div className="bg-neutral-800/10 shadow-xl rounded-lg w-full h-auto mt-6">
        <div className="relative">
          <div className="flex flex-col lg:flex-row justify-between w-full p-6 px-8 items-center h-full">
            {/* Profile Info */}
            <div className="flex flex-col lg:justify-start justify-center items-center lg:items-start mt-5 lg:mt-0 w-full">
              <div className="flex items-center">
                <p className="flex items-center text-white text-4xl font-semibold">
                  Umut Bayraktar
                </p>
              </div>
              <p className="text-white/50 text-md mt-3">
                Hi! I'm <strong>Umut</strong>, a 19-year-old software developer and content creator based in London, UK. 
                Originally from Antalya, Turkey, I specialize in technology, software, and cryptocurrency.
              </p>
            </div>

            {/* Profile Image */}
            <div className={`order-first lg:order-last flex-shrink-0 relative w-[160px] h-[160px] rounded-full pulse-avatar-online`}>
              <img
                alt="umutbayraktar"
                src={`https://ugc.production.linktr.ee/6RJk9s2pQZ2yAdcxw3Ir_TXX2dLlNmwM2OFdf?io=true&size=avatar-v3_0`}
                width="160"
                height="160"
                className={`bg-neutral-700 w-[160px] h-[160px] rounded-full`}
              />
            </div>
          </div>

          {/* Additional Info */}
          <div className="p-6 text-white">
            <h2 className="text-2xl font-semibold mt-6">Experience and Expertise</h2>
            <ul className="list-disc pl-6 mt-3">
              <li>
                <strong>Community Management:</strong> With 5 years of experience, I’ve worked on various projects, 
                building and managing communities and developing social media strategies.
              </li>
              <li>
                <strong>Software Development:</strong> As a full-stack web developer, I’ve been involved in various projects, 
                including <strong>Code Share</strong>, a public platform for sharing software.
              </li>
              <li>
                <strong>Content Creation:</strong> I create expert-level content about software and cryptocurrency on social media, 
                where I’ve gained a following of over <strong>55,000 people</strong>.
              </li>
            </ul>

            <h2 className="text-2xl font-semibold mt-6">Social Media Links</h2>
            <ul className="list-none mt-3">
              <li>
                <a href="https://facebook.com/umutxyp" target="_blank" className="text-blue-500 underline">Facebook</a>
              </li>
              <li>
                <a href="https://instagram.com/umutxyp" target="_blank" className="text-blue-500 underline">Instagram</a>
              </li>
              <li>
                <a href="https://t.me/umutland" target="_blank" className="text-blue-500 underline">Telegram</a>
              </li>
              <li>
                <a href="https://youtube.com/umutxyp" target="_blank" className="text-blue-500 underline">YouTube</a>
              </li>
            </ul>

            <h2 className="text-2xl font-semibold mt-6">Key Project</h2>
            <p className="mt-3">
              <strong>Code Share:</strong> My first project was a public platform for developers to share their software. 
              This initiative helped me gain significant experience in planning, development, and project management.
            </p>

            <h2 className="text-2xl font-semibold mt-6">My Goals and Approach</h2>
            <p className="mt-3">
              I aim to reach wider audiences by sharing knowledge in the fields of cryptocurrency and technology. 
              With a focus on innovative thinking and professionalism, I strive to make a difference, especially in 
              community management and social media.
            </p>
          </div>

          {/* Footer Text */}
          <br />
          <span
            style={{ zIndex: '-1' }}
            className="text-white/5 absolute bottom-3 left-7 text-xl sm:text-2xl md:text-4xl lg:text-3xl font-semibold"
          >
            Content Creator / Manager
          </span>
        </div>
      </div>
    </>
  );
}
