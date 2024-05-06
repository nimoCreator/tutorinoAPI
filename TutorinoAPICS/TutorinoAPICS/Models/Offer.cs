namespace TutorinoAPICS.Models
{
    public class Offer
    {
        public int id { get; set; }
        public int userID {  get; set; }
        public double price { get; set; }
        public string description {  get; set; }
    }

    public class OfferAdded
    {
        public int userID { get; set; }
        public double price { get; set; }
        public string description { get; set; }
    }
}
