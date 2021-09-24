using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ${projectName}.Models {
    [System.ComponentModel.DataAnnotations.Schema.Table("tb_scope")]
    public class Scope : AbstractEntity {
        
        [System.ComponentModel.DataAnnotations.Schema.Column("hash_sope")]
        public string HashSope {get; set;}
    }
}