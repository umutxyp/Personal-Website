export default async (req, res) => {
  const data = [
    {
      id: 1,
      image: "https://avatars.githubusercontent.com/u/82614585?s=400&u=ae44c9641228c314076aa777b8257b153dd0eb35&v=4",
      name: "Code Share",
      description: "Code Share, it offers an ideal platform for developers to share their projects, interact with other developers and sell their projects for money, exploring many projects in different categories and software languages.",
      link: "https://codeshare.me",
    },
    {
      id: 2,
      image: "https://ugc.production.linktr.ee/6RJk9s2pQZ2yAdcxw3Ir_TXX2dLlNmwM2OFdf?io=true&size=avatar-v3_0",
      name: "Social Accounts",
      description: "I am a professional editor and intermediate software developer. I have been professionally interested in community management and development for 5 years, I have high level knowledge and experience in areas such as community management and social media management. I post videos about discord on my youtube channel.",
      link: "https://linktr.ee/umutxyp",
    }
  ];
  res.status(200).json(data);
};
