http://cxf.547215.n5.nabble.com/Upgrade-throws-strange-WSDL-error-xmlns-ns0-default-is-not-a-valid-URI-td5717356.html

Fixed up my issue... 

I found that the difference between the two WSDLs included a custom exception, which had the following two annotations applied 

@XmlType 
@XmlAccessorType 

Removing those two annotations on that custom exception class cleared things up.

---

@XmlType 
@XmlAccessorType   


Is no longer the issue..  if you confuse Jaxb by using these annotations on some @XmlAccessorType(XmlAccessType.PUBLIC_MEMBER) and some with Methods and so on.. then You will run into those issues..
