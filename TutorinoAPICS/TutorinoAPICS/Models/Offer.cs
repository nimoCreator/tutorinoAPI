namespace TutorinoAPICS.Models
{
    public class Offer
    {
        public int id { get; set; }
        public int userID { get; set; }
        public int subjectID { get; set; }
        public double price { get; set; }
        public string description { get; set; }
    }

    public class OfferAdded
    {
        public int userID { get; set; }
        public int subjectID { get; set; }
        public double price { get; set; }
        public string description { get; set; }
    }

    public class OfferSubject
    {
        public int subjectID { get; set; }
    }

    public class OfferID
    {
        public int subjectID { set; get; }
        public int userID { set; get; }
    }

    public class OfferUID
    {
        public int userID { set; get; }
    }

    public class OfferIDD {
        public int offerID { get; set; }
    }
}
