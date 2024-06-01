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

    public class Offers
    {
        public string SubjectName {get;set;}   
    }

    public class OfferInfo{
        public int id {get;set;}
        public int kuid {get;set;}
        public int sid {get;set;}
        public double price {get;set;}
        public String desc {get;set;}
    }

    public class OfferPrint{
        public int id {get;set;}
    }
}
