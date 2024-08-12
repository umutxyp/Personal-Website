export default async (req, res) => {
  const data = [
    {
      id: 1,
      image: "https://codeshare.me/assets/img/favicon.png",
      name: "Code Share",
      description: "Code Share, it offers an ideal platform for developers to share their projects, interact with other developers and sell their projects for money, exploring many projects in different categories and software languages.",
      link: "https://codeshare.me",
    },
    {
      id: 2,
      image: "https://images-ext-1.discordapp.net/external/BagPBMpzrJCuIJKUSdmQ5CFusioIc9-clJBoObcUA0A/https/cdn.discordapp.com/avatars/615029465726320654/a_9a33f999daebb6e9197cf7bb6ff5f506.gif",
      name: "Social Accounts",
      description: "I am a professional editor and intermediate software developer. I have been professionally interested in community management and development for 5 years, I have high level knowledge and experience in areas such as community management and social media management. I post videos about discord on my youtube channel.",
      link: "https://linktr.ee/umutxyp",
    }
  ];
  res.status(200).json(data);
};
