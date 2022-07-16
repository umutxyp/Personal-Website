export default async (req, res) => {
  const data = [
    {
      id: 1,
      image: "https://media.discordapp.net/attachments/737348411568685066/954502826791428136/codeshare_logo.png",
      name: "Code Shop",
      description:
        "Publish your own software or images for free or for a fee. Earn money.",
      link: "https://codeshare.xyz",
    },
    {
      id: 2,
      image: "https://media.discordapp.net/attachments/737347015251460156/989673154727264296/channels4_profile.jpg",
      name: "Youtube",
      description:
        "My personal youtube channel where I post music videos.",
      link: "https://youtube.com/UmutBayraktarYT",
    },
     {
      id: 3,
      image: "https://caoscrew.com/assets/images/team/KK.jpg",
      name: "Caos Crew",
      description:
        "A magnificent and valuable nft collection of 8888 pieces.",
      link: "https://caoscrew.com/",
    }
  ];
  res.status(200).json(data);
};
