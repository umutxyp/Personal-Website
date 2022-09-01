export default async (req, res) => {
  const data = [
    {
      id: 1,
      image: "https://media.discordapp.net/attachments/737348411568685066/954502826791428136/codeshare_logo.png",
      name: "Code Share",
      description: "Discord türkiyenin en büyük discord bot komutları arşivi ve en büyük discord botu uptime, hostlayıcı websitesi. Code Share veritabanında discord botlarına özgü yüzlerce discord bot komutu bulunmaktadır ve kendi discord botunuzu yaratmanıza yardımcı olur.",
      link: "https://codeshare.me",
    },
    {
      id: 2,
      image: "https://media.discordapp.net/attachments/737348411568685066/999563078079361074/YT_AVATAR_NET.jpg",
      name: "Youtube Channel",
      description: "I am a professional editor and intermediate software developer. I have been professionally interested in community management and development for 5 years, I have high level knowledge and experience in areas such as community management and social media management. I post videos about discord on my youtube channel.",
      link: "https://youtube.com/UmutBayraktarYT",
    }
  ];
  res.status(200).json(data);
};
