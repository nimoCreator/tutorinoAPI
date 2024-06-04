namespace TutorinoAPICS.Models
{
    public class Transaction
    {
        public String status {get;set;}
        public int ouid {get;set;}
        public DateTime trans_date {get;set;}
        public double value {get;set;}
        public String currency {get;set;}
        public String details {get;set;}
    }
}
