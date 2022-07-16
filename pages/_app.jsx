import '../styles/globals.css'
import '../styles/tooltip.css'
import Head from 'next/head';
import dynamic from 'next/dynamic';
import 'tippy.js/animations/scale-subtle.css';
import 'tippy.js/animations/scale-extreme.css';
import 'tippy.js/animations/shift-away.css';
import 'tippy.js/animations/shift-toward.css';
import Router, { useRouter } from "next/router";
import { Fragment, useEffect, useState } from "react";
import { Transition } from "@headlessui/react";

const Header = dynamic(() => import('../components/Header'))
function MyApp({ Component, pageProps }) {
  let [load,setLoad] = useState(false);
    useEffect(() => {
      setTimeout(() => {
        setLoad(true);
        document.documentElement.style = 'pointer-events: all;'
      }, 1000)
    }, [])
    Router.events.on('routeChangeStart', () => {
        setLoad(false);
        document.documentElement.style = 'pointer-events: none;'
    });
    Router.events.on('routeChangeComplete', () => {
      setTimeout(() => {
        setLoad(true);
        document.documentElement.style = 'pointer-events: all;'
      }, 1000)
    });
    Router.events.on('routeChangeError', () => {
      setTimeout(() => {
        setLoad(true);
        document.documentElement.style = 'pointer-events: all;'
      }, 1000)
    });
  return (<>
    <Head>
        <title>Umut Bayraktar</title>
        <link rel="shortcut icon" href="https://media.discordapp.net/attachments/737348411568685066/954506783777493072/Umut_Bayraktar_Icon.png" type="image/x-icon" ></link>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link href="https://pro.fontawesome.com/releases/v5.15.4/css/all.css" rel="stylesheet" />

    </Head>
    <Transition
          as={Fragment}
          show={!load ? true : false}
          enter="transform transition duration-[100ms]"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="transform duration-[250ms] transition ease-in-out"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
      >
        <div style={{ zIndex: 99999 }} className="fixed bg-black/75 w-full h-screen flex justify-center items-center pointer-events-none">
            <div className="flex items-center gap-x-6 animate-pulse">
                <div className="text-center">
                    <p className="text-6xl mb-5 font-semibold">Umut Bayraktar</p>
                    <p className="uppercase text-xl font-semibold text-white"><i className="fal fa-spinner-third fa-spin" /></p>
                </div>
            </div>
        </div>
    </Transition>
    <main className="border-b-[7px] border-t-[7px] h-full border-neutral-800/50 w-full">
      <div className="min-h-screen max-w-screen-lg p-5 w-full md:w-10/12 lg:w-8/12 mx-auto transition-all duration-300">
        <Header />
        <Component {...pageProps} />
      </div>
      <div className="bg-neutral-800/5">
        <div className="max-w-screen-lg p-5 w-full md:w-10/12 lg:w-8/12 mx-auto transition-all duration-300">
          <div className="md:flex w-full items-center justify-between">
            <div>
              <p>❤️ Umut Bayraktar</p></div>
            <div className="mt-2 md:mt-0 flex items-center">
              <a href="https://discord.gg/58e5H4try3" target="_blank" rel="noreferrer" className="w-full md:w-auto bg-neutral-700/5 hover:bg-neutral-700/20 px-4 py-2 rounded-md transition-all duration-200">
                <i className="fab fa-discord mr-2" />Join My Discord
              </a>
            </div>

          </div>
        </div>
      </div>
    </main>
  </>);
}

export default MyApp
